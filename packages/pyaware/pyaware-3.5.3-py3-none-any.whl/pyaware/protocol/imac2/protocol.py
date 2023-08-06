from datetime import datetime
import os
import struct
import logging
from enum import Flag
from pathlib import Path
import time
import typing
import asyncio
from collections import defaultdict
import aiohttp
from pyaware import async_threaded
from pyaware.triggers.process import run_triggers
import pyaware.triggers
from pyaware.data_types import (
    AddressMapUint16,
    Param,
    ParamBits,
    ParamMask,
    ParamLookup,
    ParamText,
    ParamDict,
)
from pyaware.commands import Commands, ValidateIn, TopicTask, InvalidCommandData
from pyaware.protocol.imac2 import ModuleStatus
from pyaware.protocol.modbus import modbus_exception_codes
from pyaware.protocol.imac2.modules import ImacModule, module_types
from pyaware import events
from pyaware.mqtt.models import TopologyChildrenV2
import pyaware.aggregations
from pyaware.store import memory_storage

try:
    import rapidjson as json
except ImportError:
    import json

if typing.TYPE_CHECKING:
    from pyaware.triggers.collect import Deadline

log = logging.getLogger(__file__)
# Address 1036
generation_bits = {0: 0, 1: 0b1 << 8, 2: 0b1 << 9, 3: 0b11 << 8}


class ModuleStatusBits(Flag):
    ON_SCAN = 1 << 0
    L1_CLASH = 1 << 1
    GLOBAL_SELECT = 1 << 2
    L1_OWNED = 1 << 3
    L2_OWNED = 1 << 4
    SYSTEM_OWNED = 1 << 5
    L2_CLASH = 1 << 6
    BYTE_OWNED = 1 << 7


# Address 1042
remote_key = {
    0: " No Key",
    1: " ESC Key ESC_KEY",
    2: " Alarm Key ALARM_KEY",
    3: " Menu Key MENU_KEY",
    5: " F1 Key F1_KEY",
    6: " F2 Key F2_KEY",
    7: " F3 Key F3_KEY",
    8: " F4 Key F4_KEY",
    9: " Left Arrow Key LEFT_KEY",
    10: " Up Arrow Key UP_KEY",
    11: " Right Arrow Key RIGHT_KEY",
    12: " Down Arrow Key DOWN_KEY",
    13: " Enter Key ENTER_KEY",
    16: " Shift Mode Key SHIFT_MOD",
}


class TopicLock(asyncio.Lock):
    def __init__(
        self,
        *args,
        topic: str,
        acquire_state: bool = True,
        data_key: str = "",
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.topic = topic
        self.data_key = data_key
        self.acquire_state = acquire_state

    async def __aenter__(self):
        aenter = await super().__aenter__()
        if self.data_key:
            parameters = {self.data_key: self.acquire_state}
        else:
            parameters = self.acquire_state
        pyaware.events.publish(self.topic, data=parameters, timestamp=datetime.utcnow())
        return aenter

    async def __aexit__(self, *args, **kwargs):
        aexit = await super().__aexit__(*args, **kwargs)
        if self.data_key:
            parameters = {self.data_key: not self.acquire_state}
        else:
            parameters = not self.acquire_state
        pyaware.events.publish(self.topic, data=parameters, timestamp=datetime.utcnow())
        return aexit


class ConditionalLock:
    """
    Implements conditional lock acquisition for asyncio.Lock()
    usage:
    >>>x = 1
    >>>l = ConditionalLock(lambda: x == 2)
    >>>async def set_x():
    >>>    await asyncio.sleep(5)
    >>>    global x
    >>>    x = 2
    >>>async def main():
    >>>    global x
    >>>    x = 1
    >>>    asyncio.create_task(set_x())
    >>>    async with l:
    >>>        print(f"Acquired @ x=={x}")
    >>>
    >>>asyncio.create_task(main())

    :param predicate A callable that should return True when the lock should be acquired
    :param lock A asyncio Lock that can be shared across multiple conditional locks. If not provided, will use as new
    :param check_condition_after Time to wait after a failed predicate call before trying to reacquire the lock
    lock
    """

    def __init__(
        self,
        predicate: typing.Callable,
        *args,
        lock: typing.Optional[asyncio.Lock] = None,
        check_condition_after: float = 0.1,
        **kwargs,
    ):
        self.lock = lock or asyncio.Lock()
        self.predicate = predicate
        self.check_condition_after = check_condition_after
        super().__init__(*args, **kwargs)

    async def __aenter__(self):
        try:
            while True:
                aenter = await self.lock.acquire()
                if self.predicate():
                    break
                self.lock.release()
                await asyncio.sleep(self.check_condition_after)
        except BaseException:
            if self.lock.locked():
                self.lock.release()
            raise
        return aenter

    async def __aexit__(self, *args, **kwargs):
        if self.lock.locked():
            self.lock.release()


@events.enable
class Imac2Protocol:
    name = "Imac Controller"
    module_type = "imac-controller-master"
    config_name = "imac_parameter_spec.yaml"

    def __init__(self, client_ser, device_id: str, client_eth=None, unit=1):
        """
        :param client_ser: Client connected to the iMAC serial interface
        :param client_eth: Client connection to the iMAC2 Ethernet connection
        :param unit: Modbus unit id for the ModbusRTU connection
        """
        self.config_path = (
            Path(pyaware.__file__).parent
            / "devices"
            / "ampcontrol"
            / "imac"
            / self.config_name
        )
        self.config = pyaware.config.load_config(self.config_path)
        self.schedule_reads: typing.Dict[str, Deadline] = {}
        self.poll_interval = 1
        self.client_ser = client_ser
        self.client_eth = client_eth
        self.unit = unit
        # TODO load from store
        self.devices: {str: ImacModule} = {}
        self.data_point_blocks = self._modbus_ranges(
            (0, 0x47F), (0x500, 0x580), (0x600, 0x6A2)
        )
        # TODO move to module detection routine because software version and hardware version is not on GG2
        self.roll_call_params = {
            "generation_id": ParamMask(
                0x409, "generation_id", mask=0b11 << 8, rshift=8
            ),
            "serial_number": Param(0x40B, "serial_number"),
            "module_type": ParamMask(0x40C, "module_type", mask=0xFF),
            "imac_address": ParamMask(0x40A, "imac_address", mask=0xFF),
            "version": ParamMask(0x40C, "version", mask=0xFF00, rshift=8),
        }
        self.device_id = device_id
        self.current_state = {
            "master-fieldbus-number": int(self.device_id.split("-")[-1])
        }
        self.store_state = {}
        self.send_state = {}
        self.event_state = {}
        self._block_lock = asyncio.Lock()
        self.block_condition = {
            None: ConditionalLock(lambda: True, lock=self._block_lock),
            0: ConditionalLock(
                lambda: self.roll_call_gen in [None, 0], lock=self._block_lock
            ),
            1: ConditionalLock(
                lambda: self.roll_call_gen in [None, 1], lock=self._block_lock
            ),
            2: ConditionalLock(
                lambda: self.roll_call_gen in [None, 2], lock=self._block_lock
            ),
            3: ConditionalLock(
                lambda: self.roll_call_gen in [None, 3], lock=self._block_lock
            ),
        }
        self.roll_call_gen = None
        self.commands = Commands({}, device_id=device_id)
        self.auto_discover_lock = asyncio.Lock()
        self.roll_call_lock = TopicLock(
            topic="imac_controller_data",
            data_key="roll-call-active",
            acquire_state=True,
        )
        self.commands.update(
            {
                "find-modules": [
                    ValidateIn(range(256)),
                    TopicTask(topic="find_modules", key_map={"data": "address"}),
                ],
                "find-serial": [
                    TopicTask(
                        topic="find_serial",
                        key_map={"data": "serial"},
                        include_cmd_as_key="cmd",
                    ),
                ],
                "clear-address": [
                    ValidateIn(range(256)),
                    TopicTask(topic="clear_address", key_map={"data": "address"}),
                ],
                "sync-rtc": [
                    TopicTask(topic="sync_rtc", key_map={"timestamp": "value"})
                ],
                "boundary-enable": [
                    TopicTask(topic=f"boundary_enable/{id}", key_map={"data": "value"}),
                ],
                "remote-bypass-gg2": [
                    ValidateIn(range(1, 41), key="address"),
                    ValidateIn(range(2), key="value"),
                    TopicTask(
                        topic="remote_bypass_gg2",
                        key_map={"logical_address": "address", "value": "value"},
                    ),
                ],
                "remote-bypass-rts": [
                    ValidateIn(range(1, 13), key="address"),
                    ValidateIn(range(2), key="value"),
                    TopicTask(
                        topic="remote_bypass_rts",
                        key_map={"logical_address": "address", "value": "value"},
                    ),
                ],
                "plc-trip-reset": [
                    TopicTask(topic="plc_trip_reset"),
                ],
                "trip-reset": [
                    TopicTask(topic="trip_reset"),
                ],
            }
        )
        self.controller_data = {
            "system-status": ParamBits(
                0x100,
                bitmask={
                    "control-relay-state": 8,
                    "auxiliary-relay-state": 9,
                    "l1-short-circuit-status": 12,
                },
            ),
            "system-control": ParamBits(
                0x400,
                bitmask={
                    "master-backtrip-bypass": 4,
                },
            ),
            "system-id": ParamBits(
                0x401,
                bitmask={"dip-sw-1": 4, "dip-sw-2": 5, "dip-sw-3": 6, "dip-sw-4": 7},
            ),
            "rotary-sw": ParamMask(0x401, "rotary-sw", mask=0xF),
            "l1-data-block-just-complete": Param(0x406, "l1-data-block-just-complete"),
            "slp-loop-timer": Param(0x408, "slp-loop-timer"),
            # NVM
            "serial-protocol": ParamLookup(
                0x500,
                "serial-protocol",
                mask=0xFF,
                table={
                    0: "not-configured",
                    1: "modbus-master",
                    2: "modbus-slave",
                    3: "ip2-protocol",
                    4: "l1-maintenance",
                    5: "l2-maintenance",
                },
                table_reversed={
                    "modbus-master": 1,
                    "modbus-slave": 2,
                    "ip2-protocol": 3,
                    "l1-maintenance": 4,
                    "l2-maintenance": 5,
                },
            ),
            "serial-baud-rate": ParamLookup(
                0x500,
                "serial-baud-rate",
                mask=0xFF00,
                rshift=8,
                table={
                    0: 9600,
                    1: 0,
                    2: 600,
                    3: 1200,
                    4: 2400,
                    5: 4800,
                    6: 9600,
                    7: 19200,
                },
                table_reversed={
                    600: 2,
                    1200: 3,
                    2400: 4,
                    4800: 5,
                    9600: 6,
                    1920: 7,
                },
            ),
            "serial-parity": ParamLookup(
                0x501,
                "serial-parity",
                mask=0xFF,
                table={0: "even", 1: "none", 2: "even", 3: "odd"},
                table_reversed={
                    "none": 1,
                    "even": 2,
                    "odd": 3,
                    "n": 1,
                    "e": 2,
                    "o": 3,
                    "N": 1,
                    "E": 2,
                    "O": 3,
                },
            ),
            "serial-stop-bits": ParamLookup(
                0x501,
                "serial-stop-bits",
                mask=0xFF00,
                rshift=8,
                table={0: 1, 1: 1, 2: 2},
                table_reversed={1: 1, 2: 2},
            ),
            "serial-mode": ParamLookup(
                0x502,
                "serial-mode",
                mask=0xFF,
                table={0: "RS232", 1: "RS485/RS422"},
                table_reversed={"RS232": 0, "RS485": 1, "RS422": 2, "RS485/RS422": 3},
            ),
            "serial-slave-address": ParamMask(
                0x502, "serial-slave-address", mask=0xFF00, rshift=8
            ),
            "controller-hardware-flags": ParamBits(
                0x600, bitmask={"rtc-fault": 0, "i2c-fault": 1, "sc-card-fault": 2}
            ),
            "controller-temperature": Param(
                0x601, "controller-temperature", scale=0.01
            ),
            "controller-tag-name": ParamText(
                0x638,
                "controller-tag-name",
                length=19,
                padding=b"\xa5",
                swap_bytes=True,
            ),
            "legacy-hardware-version": ParamText(
                0x64C,
                "legacy-hardware-version",
                length=10,
                padding=b"\xa5",
                swap_bytes=True,
            ),
            "legacy-firmware-version": ParamText(
                0x656,
                "legacy-firmware-version",
                length=10,
                padding=b"\xa5",
                swap_bytes=True,
            ),
            "legacy-software-version": ParamText(
                0x660,
                "legacy-software-version",
                length=10,
                padding=b"\xa5",
                swap_bytes=True,
            ),
            "slp-version": ParamText(
                0x66A, "slp-version", length=10, padding=b"\xa5", swap_bytes=True
            ),
            "log-bootloader-name": ParamText(
                0x674, "log-bootloader-name", length=8, padding=b"\x00", swap_bytes=True
            ),
            "log-bootloader-version": ParamText(
                0x67C,
                "log-bootloader-version",
                length=3,
                padding=b"\xa5",
                swap_bytes=True,
            ),
            "log-hardware-name": ParamText(
                0x67F,
                "log-hardware-name",
                length=8,
                padding=b" ",
                swap_bytes=True,
                strip_lagging=" ",
            ),
            "log-hardware-version": ParamText(
                0x689,
                "log-hardware-version",
                length=3,
                padding=b"\xa5",
                swap_bytes=True,
            ),
            "serial-number": ParamText(
                0x68A,
                "serial-number",
                length=8,
                padding=b"\xa5",
                swap_bytes=True,
                strip_leading="0",
            ),
            "log-application-name": ParamText(
                0x692,
                "log-application-name",
                length=8,
                padding=b"\x00",
                swap_bytes=True,
            ),
            "log-application-version": ParamText(
                0x69A,
                "log-application-version",
                length=8,
                padding=b"\x00",
                swap_bytes=True,
            ),
            "master-fieldbus-number": Param(0x523, "master-fieldbus-number"),
            "plc-activity-word": Param(0x525, "plc-activity-word"),
            "trip-flags": ParamBits(
                0x530,
                bitmask={
                    "mgm-gas-trip": 0,
                    "slave-surface-trip": 1,
                },
            ),
        }
        self.rest_data = {
            "ethernet-dhcp": ParamDict(
                "P_DHCP", "ethernet-dhcp", table={"No": False, "Yes": True}
            ),
            "ethernet-ip-address": ParamDict("P_IP_Address", "ethernet-ip-address"),
            "ethernet-ip-mask": ParamDict("P_IP_Mask", "ethernet-ip-mask"),
            "ethernet-ip-gateway": ParamDict("P_Gateway", "ethernet-ip-gateway"),
            "ethernet-mac-address": ParamDict("P_MAC_Address", "ethernet-mac-address"),
            "l1-line-speed": ParamDict(
                "P_L1_Speed",
                "l1-line-speed",
                table={"300": 300, "500": 500, "750": 750, "1000": 1000},
            ),
        }
        self.triggers = pyaware.triggers.build_from_device_config(
            self.config_path,
            device_id=device_id,
            send_state=self.send_state,
            store_state=self.store_state,
            event_state=self.event_state,
            current_state=self.current_state,
        )
        self.aggregates = pyaware.aggregations.build_from_device_config(
            self.config_path
        )
        self.schema = pyaware.config.load_config(
            os.path.join(os.path.dirname(__file__), "ensham_schema.yaml")
        )
        asyncio.create_task(
            self.set_fieldbus_address(int(self.device_id.split("-")[-1]))
        )
        asyncio.create_task(self.trigger_poll())
        asyncio.create_task(self.trigger_rest())
        asyncio.create_task(self.trigger_blocks())
        asyncio.create_task(self.trigger_heartbeat())

    @events.subscribe(topic="set_fieldbus_address")
    async def set_fieldbus_address(self, data):
        try:
            if not 0 < data < 1 << 16:
                raise ValueError
        except (TypeError, ValueError):
            raise pyaware.commands.ValidationError("Invalid fieldbus addreses")
        while True:
            try:
                await self.write(0x523, data)
                return
            except asyncio.CancelledError:
                log.info("Shutting down without having set the master fieldbus address")
                return
            except:
                await asyncio.sleep(1)

    def _modbus_ranges(self, *ranges, max_block=125):
        return [
            (x, min([max_block, stop - x]))
            for start, stop in ranges
            for x in range(start, stop, max_block)
        ]

    async def trigger_poll(self):
        loop = asyncio.get_running_loop()
        start = loop.time()
        log.info("Starting imac master bus polling")
        while True:
            if pyaware.evt_stop.is_set():
                log.info("Closing imac master polling")
                return
            try:
                await asyncio.sleep(start - loop.time() + self.poll_interval)
                start = loop.time()
                await self.poll_pipeline()
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning("iMAC master poll cancelled without stop signal")
                    continue
            except BaseException as e:
                if not pyaware.evt_stop.is_set():
                    log.exception(e)

    async def trigger_rest(self):
        log.info("Starting imac master rest polling")
        while True:
            if pyaware.evt_stop.is_set():
                log.info("Stop signal received, closing imac master rest calls")
                return
            try:
                await asyncio.sleep(5)
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"http://{self.client_eth.host}/cgi-bin/deviceinfo.cgi"
                    ) as response:
                        text_obj = await response.read()
                        json_obj = json.loads(text_obj.decode("utf-8", "ignore"))
                        parameters = {}
                        for param_spec in self.rest_data.values():
                            parameters.update(
                                {k: v for k, v in param_spec.decode(json_obj).items()}
                            )
                        pyaware.events.publish(
                            "imac_controller_data",
                            data=parameters,
                            timestamp=datetime.utcnow(),
                        )
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning("iMAC master rest calls cancelled without stop signal")
                    continue
            except BaseException as e:
                if not pyaware.evt_stop.is_set():
                    log.error(e)

    async def trigger_heartbeat(self):
        value = 1
        log.info("Starting imac master plc heartbeat writes")
        while True:
            if pyaware.evt_stop.is_set():
                log.info("Closing imac master heartbeat")
                return
            try:
                await asyncio.sleep(30)
                await self.write(0x525, value)
                value = (value % 1000) + 1
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning(
                        "iMAC master plc heartbeat cancelled without stop signal"
                    )
                    continue
            except BaseException as e:
                if not pyaware.evt_stop.is_set():
                    log.exception(e)

    async def trigger_blocks(self):
        """
        Schedules block and force_roll call based on deadline.
        :return:
        """
        loop = asyncio.get_running_loop()
        wait_time = 5
        start = loop.time()
        log.info("Starting imac master block reads")
        while True:
            if pyaware.evt_stop.is_set():
                log.info("Closing imac master scheduled device parameter reads")
                return
            try:
                sleep_time = start - loop.time() + wait_time
                if sleep_time < 0:
                    sleep_time = 0
                await asyncio.sleep(sleep_time)
                start = loop.time()
                # Get item from list
                try:
                    itm = min(self.schedule_reads.values())
                except ValueError:
                    continue
                await self.devices.get(itm.device).read_parameters({itm.param})
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning("iMAC master block reads cancelled without stop signal")
                    continue
            except BaseException as e:
                if not pyaware.evt_stop.is_set():
                    log.exception(e)

    @events.subscribe(topic="imac_controller_data")
    async def process_module_data_triggers(self, data, timestamp):
        self.update_current_state(data)
        store_data, send_data, event_data = await asyncio.gather(
            run_triggers(
                self.triggers.get("process", {}).get("store", []), data, timestamp
            ),
            run_triggers(
                self.triggers.get("process", {}).get("send", []), data, timestamp
            ),
            run_triggers(
                self.triggers.get("process", {}).get("event", []), data, timestamp
            ),
        )
        if store_data:
            memory_storage.update(store_data, topic=f"{self.device_id}")
            self.update_store_state(store_data)
        if send_data:
            memory_storage.update(send_data, topic=f"{self.device_id}")
            cached_data = memory_storage.pop(f"{self.device_id}")
            aggregated_data = pyaware.aggregations.aggregate(
                cached_data, self.aggregates
            )
            events.publish(
                f"trigger_send/{self.device_id}",
                data=aggregated_data,
                meta=self.dict(),
                timestamp=timestamp,
                topic_type="telemetry",
            )
            self.update_send_state(cached_data)
        if event_data and self.current_state.get("serial-number"):
            for param, value in event_data.items():
                events.publish(
                    f"parameter_trigger/{self.current_state['serial-number']}/{param}",
                    data=next(iter(value.values())),
                    timestamp=timestamp,
                )
            self.event_state.update(event_data)

    async def poll_pipeline(self):
        """
        Pipeline that begins when a pipeline is published
        :param data:
        :return:
        """
        addr_map, timestamp = await self.poll_once()
        events.publish("imac_poll_data", data=addr_map, timestamp=timestamp)
        module_data, module_status, controller_data = await asyncio.gather(
            self.process_module_data(addr_map, timestamp),
            self.process_module_status(addr_map, timestamp),
            self.process_controller_data(addr_map, timestamp),
        )
        # TODO process the imac metadata from poll here with asyncio.gather
        events.publish("imac_module_data", data=module_data, timestamp=timestamp)
        events.publish("imac_module_status", data=module_status, timestamp=timestamp)
        events.publish(
            "imac_controller_data", data=controller_data, timestamp=timestamp
        )
        events.publish("trigger_safe_gas")
        self.update_module_current_state(module_data)

    async def roll_call(self) -> [AddressMapUint16]:
        """
        Roll call the imac to discover the modules on the line
        1. Assert the “Reset Rollcall” bit (0x409: Bit 0) and wait for the bit to be cleared by the system.
        2. Read the Rollcall Control Word.
        3. Assert the “Next Rollcall” bit (0x409: Bit 1), preserving bits 8 to 15 you read in the previous step, and
           wait for the bit to be cleared by the system.
        4. Confirm that the “Rollcall Fail” (0x409: Bit 5) bit is not set.
        5. Module data will now be available in registers 1033 to 1041 (0x409 to 0x411). Richard says false
        6. The next module can be rollcalled by repeating steps 2 to 5. This process can be repeated until the
           Serial Number register (0x40B) reads as 0, indicating that all modules have been rollcalled. Modules
           will roll call in order of address followed by serial number, from highest to lowest.
        :return: List of address map parameters from addresses 0x409-0x411
        """
        # 1 Asset reset roll call
        async with self.roll_call_lock:
            async with self.block_condition[None]:
                await self.set_bit(0x409, 0)
                await self.wait_on_bit(0x409, 0, check_to=False)
                self.roll_call_gen = None

            # Return modules as they are found
            async for mod in self.roll_call_next():
                yield mod
            self.roll_call_gen = None

    async def roll_call_next(self) -> typing.AsyncIterable[AddressMapUint16]:
        prev_roll = [0] * 4
        while True:
            # 3 Assert next roll call bit
            async with self.block_condition[None]:
                await self.set_bit(0x409, 1)
                await self.wait_on_bit(0x409, 1, check_to=False, timeout=10)
                # 4 Check for roll call fail bit
                await self.check_bit(0x409, 5, check_to=False)
                addr_map = await self.read_ser(0x409, 9)
                self.roll_call_gen = (addr_map[0x409] & (0b11 << 8)) >> 8

            if addr_map[0x40B] == 0:
                # 6 All modules have been roll called
                break
            new_roll = addr_map[0x409:0x40D]
            if new_roll != prev_roll:
                yield addr_map
            prev_roll = new_roll

    async def roll_call_force(self, address) -> [AddressMapUint16]:
        """
        Roll call the imac to discover the modules on the line
        1. Assert the “Reset Rollcall” bit (0x409: Bit 0) and wait for the bit to be cleared by the system.
        2. Read the Rollcall Control Word.
        3. Assert the “Next Rollcall” bit (0x409: Bit 2), preserving bits 8 to 15 you read in the previous step, and
           wait for the bit to be cleared by the system.
        4. Confirm that the “Rollcall Fail” (0x409: Bit 5) bit is not set.
        5. Module data will now be available in registers 1033 to 1041 (0x409 to 0x411). Richard says false
        6. The next module can be rollcalled by repeating steps 2 to 5. This process can be repeated until the
           Serial Number register (0x40B) reads as 0, indicating that all modules have been rollcalled. Modules
           will roll call in order of address followed by serial number, from highest to lowest.
        :return: List of address map parameters from addresses 0x409-0x411
        """
        # 1 Asset reset roll call
        async with self.roll_call_lock:
            async with self.block_condition[None]:
                await self.write(0x40A, address)
                await self.set_bit(0x409, 0)
                await self.wait_on_bit(0x409, 0, check_to=False)
                self.roll_call_gen = None
            async for mod in self.roll_call_force_next():
                yield mod
            self.roll_call_gen = None

    async def roll_call_force_next(self) -> typing.AsyncIterable[AddressMapUint16]:
        prev_roll = [0] * 4
        while True:
            # 3 Assert next roll call bit
            async with self.block_condition[None]:
                await self.set_bit(0x409, 2)
                await self.wait_on_bit(0x409, 2, check_to=False, timeout=10)
                # 4 Check for roll call fail bit
                await self.check_bit(0x409, 5, check_to=False)
                addr_map = await self.read_ser(0x409, 9)
                self.roll_call_gen = (addr_map[0x409] & (0b11 << 8)) >> 8
            if addr_map[0x40B] == 0:
                # 6 All modules have been roll called
                break
            new_roll = addr_map[0x409:0x40D]
            if new_roll != prev_roll:
                yield addr_map
            prev_roll = new_roll

    @events.subscribe(topic="find_modules")
    async def find_modules(self, data):
        await self.auto_discover_modules(
            data={data: self.current_state["address-status"][data]}
        )

    @events.subscribe(topic="find_serial")
    async def find_serial(self, data, cmd):
        """
        Find device by serial number
        :param data: Serial number of the form X-GY
        Where X is the serial between 1-65535 and Y is is the generation between 1-4

        Finds the serial numbered device by reading by serial number at block 0
        Param 1 is the address
        Discovers modules at that address
        :return:
        """
        cmd["return_values"]["serial"] = data
        cmd["return_values"]["type"] = None
        cmd["return_values"]["name"] = None
        cmd["return_values"]["status"] = False
        try:
            serial, gen = data.split("-G")
            serial = int(serial)
            gen = int(gen) - 1
            assert 1 <= serial <= 65535
            assert 0 <= gen <= 3
        except:
            raise InvalidCommandData(
                f"Invalid serial number: {data} must be of the form XXXXX-GX"
            )
        try:
            addr_map = await self.read_by_serial_number(
                serial_number=serial, generation=gen, block=0
            )
        except ValueError as e:
            if "Bit check failed" in e.args[0]:
                return
            raise
        module_address = addr_map[1038]
        async with self.auto_discover_lock:
            async for mod in self.discover_at_address(module_address):
                if mod.current_state["dev-id"] == data:
                    cmd["return_values"]["type"] = mod.module_type
                    cmd["return_values"]["name"] = mod.name
                    cmd["return_values"]["status"] = True
                    return

    async def update_devices(self, modules: [dict]):
        """
        Updates the devices from a roll call
        :param roll_call: A list of address maps with data from the roll call addresses
        :return: None
        """
        devs = defaultdict(set)
        for imac_module in modules:
            dev_id = imac_module["dev_id"]
            if dev_id in self.devices:
                self.update_device(**imac_module)
            else:
                self.add_device(**imac_module)
            devs[dev_id].add(imac_module.get("module_type"))
        for dev_id in devs:
            try:
                await self.devices[dev_id].find_missing_starting_data()
            except asyncio.CancelledError:
                raise
            except BaseException as e:
                if pyaware.evt_stop.is_set():
                    raise
                log.error(e)
            log.info(f"Added {self.devices[dev_id]}")
        if devs:
            self.update_topology()
        return devs

    def decode_roll_call(self, roll_call: [AddressMapUint16]) -> [dict]:
        return [self.decode_roll_call_single(roll) for roll in roll_call]

    def decode_roll_call_single(self, roll_call: AddressMapUint16) -> dict:
        params = {}
        for param in self.roll_call_params.values():
            params.update(param.decode(roll_call))
        params["dev_id"] = f"{params['serial_number']}-G{params['generation_id'] + 1}"
        return params

    def update_device(self, dev_id, **kwargs):
        """
        Update the device from roll call if any of the meta data of the device has changed
        :param dev_id:
        :param kwargs:
        :return:
        """
        if any(
            self.devices[dev_id].current_state.get(kwarg) != kwargs[kwarg]
            for kwarg in kwargs
        ):
            self.devices[dev_id].update_from_roll_call(dev_id=dev_id, **kwargs)
            self.commands.sub_commands[dev_id] = self.devices[dev_id].commands

    def update_topology(self):
        children = [dev.identify() for dev in self.devices.values()]
        payload = TopologyChildrenV2(
            serial=self.current_state.get("serial-number", ""),
            type=self.module_type,
            values={},
            children=children,
        )
        events.publish(
            f"device_topology/{self.device_id}",
            data=payload,
            timestamp=datetime.utcnow(),
        )

    def add_device(self, dev_id, module_type, **kwargs):
        """
        Add the device to the imac protocol. This will allow the imac data poll to interpret the data from the device
        :param dev_id:
        :param module_type:
        :param version:
        :param kwargs:
        :return:
        """
        self.devices[dev_id] = module_types.get(module_type, ImacModule)(
            protocol=self, dev_id=dev_id
        )
        self.update_device(dev_id, module_type=module_type, **kwargs)

    async def read_by_serial_number(
        self, serial_number, generation, block=0
    ) -> AddressMapUint16:
        """
        :param serial_number: 16 bit serial number excluding generation
        :param generation: imac module generation indexed from zero. ie. Gen 2 is 1
        :param block:
        Read the parameters of a serial numbered item
        1. Ensure that the Rollcall Serial Number register (40Bh), the Generation ID (409h bits 8 & 9) and the
           Rollcall Block Number register (40Dh) are set up as per the module that is to be read.
        2. Assert the “Read Serial Number” bit (409h: Bit 3), preserving Generation ID bits 8 & 9 setup in step
        1, and wait for the bit to be cleared by the system
        3. Confirm that the “Read SN Fail” (409h: Bit 6) bit is not set.
        4. Module Parameters 1, 2, 3 and 4 will now be available in registers 1038 to 1041 (40Eh to 411h).
        :return: Address map of 4 parameters from registers 0x40E to 0x411
        """
        async with self.block_condition[generation]:
            reg_roll_coll = await self.read_ser_single(0x409)
            await self.write(0x40B, serial_number)
            await self.write(0x409, (reg_roll_coll & ~(0b11 << 8)) | (generation << 8))
            await self.write(0x40D, block)
            # 2 Assert read serial number
            await self.set_bit(0x409, 3)
            await self.wait_on_bit(0x409, 3, False)
            await self.check_bit(0x409, 6, False)
            return await self.read_ser(0x409, 9)

    async def write_by_serial_number(
        self, serial_number, generation, block, addr_map: AddressMapUint16
    ):
        """
        1. Ensure that the Rollcall Serial Number register (40Bh), the Generation ID (409h bits 8 & 9) and the
           Rollcall Block Number register (40Dh) are set up as per the module that is to be written.
        2. Ensure the parameters that are to be written to the module are set up in registers 1038 to 1041
           (40Eh to 410h).
        3. Assert the “Write Serial Number” bit (409h: Bit 4), preserving Generation ID bits 8 & 9 setup in step
           1, and wait for the bit to be cleared by the system.
        4. Confirm that the “Write SN Fail” (409h: Bit 7) bit is not set.
        External to this command, a check should be performed to ensure that the parameters were successfully written.
        5. Wait for block scan register 0x406 increment twice (Heartbeat).
           Note: can take a while so you can write multiple serials and then bulk check them after the 2 block scans
        6. Module Parameters 1,2,3, and 4 will now have been successfully written to the module from
        registers 1038 to 1041 (40Eh to 411h).
        :return:
        """
        async with self.block_condition[generation]:
            reg_roll_coll = await self.read_ser_single(0x409)
            await self.write(0x40B, serial_number)
            await self.write(0x409, (reg_roll_coll & ~(0b11 << 8)) | (generation << 8))
            await self.write(0x40D, block)
            await self.write(0x409, *addr_map[0x409:0x412])
            # 3 Assert write serial number
            await self.set_bit(0x409, 4)
            await self.wait_on_bit(0x409, 4, False)
            # 4 Confirm write SN Fail bit not set
            await self.check_bit(0x409, 7, False)

    async def write_by_serial_number_no_check(
        self, serial_number, generation, block, addr_map: AddressMapUint16
    ):
        """
        Does a write by serial number with no confirmation of the bit 4 being cleared. This can be done for more time
        critical writes where it will be obvious it has not
        1. Ensure that the Rollcall Serial Number register (40Bh), the Generation ID (409h bits 8 & 9) and the
           Rollcall Block Number register (40Dh) are set up as per the module that is to be written.
        2. Ensure the parameters that are to be written to the module are set up in registers 1038 to 1041
           (40Eh to 410h).
        :return:
        """
        async with self.block_condition[generation]:
            reg_roll_coll = await self.read_ser_single(0x409)
            await self.write(0x40B, serial_number)
            await self.write(0x409, (reg_roll_coll & ~(0b11 << 8)) | (generation << 8))
            await self.write(0x40D, block)
            await self.write(0x409, *addr_map[0x409:0x412])
            # 3 Assert write serial number
            await self.set_bit(0x409, 4)

    async def read(self, client, address: int, count: int = 1) -> AddressMapUint16:
        """
        Reads modbus holding registers and returns an address map of the response
        :param address:
        :param count:
        :return:
        """
        rr = await client.read_holding_registers(address, count, unit=self.unit)
        if rr.isError():
            raise modbus_exception_codes.get(rr.exception_code, IOError)
        addr_map = AddressMapUint16()
        addr_map[address : address + count] = rr.registers
        return addr_map

    async def read_eth(
        self, address: int, count: int = 1
    ) -> typing.Union[AddressMapUint16, typing.Awaitable]:
        """
        Reads modbus holding registers and returns an address map of the response
        :param address:
        :param count:
        :return:
        """
        try:
            res = await self.read(self.client_eth.protocol, address, count)
            events.publish(
                "imac_controller_data",
                data={"ethernet-comms-status": True},
                timestamp=datetime.utcnow(),
            )
            return res
        except AttributeError:
            events.publish(
                "imac_controller_data",
                data={"ethernet-comms-status": False},
                timestamp=datetime.utcnow(),
            )
        except asyncio.CancelledError:
            raise
        except BaseException as e:
            events.publish(
                "imac_controller_data",
                data={"ethernet-comms-status": False},
                timestamp=datetime.utcnow(),
            )
            if self.client_eth.connected:
                log.exception(e)
            raise
        return AddressMapUint16()

    async def read_ser_single(self, address) -> int:
        read = await self.read_ser(address, 1)
        return read[address]

    async def write_bit(self, address, bit, value):
        if hasattr(self.client_ser, "protocol"):
            client = self.client_ser.protocol
        else:
            client = self.client_ser
        wr = await client.write_coil(address * 16 + bit, value, unit=self.unit)
        if wr.isError():
            raise modbus_exception_codes.get(wr.exception_code, IOError)

    async def poll_once(self) -> typing.Tuple[AddressMapUint16, datetime]:
        """
        Perform a complete poll of the imac data
        :requires: client_eth to be available
        :return:
        """
        addr_map = AddressMapUint16()
        for address, count in self.data_point_blocks:
            addr_map.merge(await self.read_eth(address, count))
        return addr_map, datetime.utcnow()

    def process_poll(self, addr_map: AddressMapUint16):
        """
        Process the results from a poll_once call.
        Grouped in categories
        "system-data"
        "module-data":
        "system-runtime-variables"
        "nvm-variables"
        "nvm-user"
        "controller-information"

        Module data should be
        :param addr_map:
        :return:
        """

    @async_threaded
    def process_module_data(self, addr_map: AddressMapUint16, timestamp: datetime):
        """
        :param addr_map: address map returned from poll_once or poll_once_async
        :return: dictionary of parameter data indexed by imac serial number
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
        module_data = {
            f"{dev.current_state['dev-id']}": dev.process_module_data(
                addr_map, timestamp
            )
            for dev in self.devices.values()
        }
        return module_data

    @async_threaded
    def process_module_status(self, addr_map: AddressMapUint16, timestamp: datetime):
        """
        Process the module status registers and trigger messages based on status changes
        :param addr_map:
        :param timestamp:
        :return:
        """
        status = {
            "address-status": [
                self.parse_status(addr_map[x + 0x100]) for x in range(1, 0x100)
            ],
            "address-status-raw": addr_map[0x100:0x200],
            "address-resistance": [addr_map[x + 0x200] for x in range(0x100)],
        }
        # Make address 0 always System Status
        status["address-status"].insert(0, ModuleStatus.SYSTEM)
        return status

    @async_threaded
    def process_controller_data(self, addr_map: AddressMapUint16, timestamp: datetime):
        """
        Process
        :param addr_map:
        :param timestamp:
        :return:
        """
        parameters = {}
        for param_spec in self.controller_data.values():
            parameters.update({k: v for k, v in param_spec.decode(addr_map).items()})
        return parameters

    @events.subscribe(topic="trigger_safe_gas", in_thread=True)
    def process_safe_gas(self):
        """
        :return:
        """
        resp = [-2000] * 40
        for serial, dev in self.devices.items():
            if dev.module_type == "imac-module-gg2":
                try:
                    resp[dev.current_state["address-analog"] - 41] = dev.current_state[
                        "detector-gas-analog-safe-gas"
                    ]
                except (KeyError, IndexError):
                    pass
        events.publish("mqtt_topic_send", mqtt_topic="safe-gas", msg=json.dumps(resp))

    def update_module_current_state(self, module_data: dict):
        for serial, data in module_data.items():
            self.devices[serial].update_current_state(data)

    async def set_bit(self, address, bit):
        await self.write_bit(address, bit, 1)
        if not (1 << bit) & await self.read_ser_single(address):
            raise IOError(
                "Bit not set correctly, check if someone is interfering with the device"
            )

    async def clear_bit(self, address, bit):
        await self.write_bit(address, bit, 0)
        if not (1 << bit) & ~await self.read_ser_single(address):
            raise IOError(
                "Bit not cleared correctly, check if someone is interfering with the device"
            )

    async def check_bit(self, address, bit, check_to):
        if not await self.read_ser_single(address) >> bit & 1 == check_to:
            raise ValueError(
                "Bit check failed, imac module failed to communicate with the master"
            )

    async def wait_on_bit(self, address, bit, check_to, timeout=3):
        start = time.time()
        last_attempt = False
        while True:
            try:
                await self.check_bit(address, bit, check_to)
                return
            except (IOError, ValueError):
                if time.time() - start > timeout:
                    if last_attempt:
                        break
                    last_attempt = True
        raise TimeoutError("Timeout waiting for bit check")

    async def read_ser(self, address: int, count: int = 1) -> AddressMapUint16:
        """
        Reads modbus holding registers and returns an address map of the response
        :param address:
        :param count:
        :return:
        """
        if hasattr(self.client_ser, "protocol"):
            client = self.client_ser.protocol
        else:
            client = self.client_ser
        try:
            res = await self.read(client, address, count)
            events.publish(
                "imac_controller_data",
                data={"serial-comms-status": True},
                timestamp=datetime.utcnow(),
            )
            return res
        except:
            events.publish(
                "imac_controller_data",
                data={"serial-comms-status": False},
                timestamp=datetime.utcnow(),
            )
            raise

    async def write(self, address, *values):
        if hasattr(self.client_ser, "protocol"):
            client = self.client_ser.protocol
        else:
            client = self.client_ser
        wr = await client.write_registers(address, values, unit=self.unit)
        if wr.isError():
            raise modbus_exception_codes.get(wr.exception_code, IOError)

    @events.subscribe(topic="boundary_enable/{id}")
    async def boundary_enable(self, data):
        """
        :param data: 40 bit sequence in an array corresponding to detectors 1-40
        :param timestamp:
        :return:
        """
        if len(data) != 40:
            raise ValueError
        addr_map = AddressMapUint16()
        addr_map[0x520:0x523] = 0, 0, 0
        for index, bit in enumerate(data):
            address = 0x520 + index // 16
            addr_map[address] |= bit << (index % 16)
        await self.write(0x520, *addr_map[0x520:0x523])

    @events.subscribe(topic="remote_bypass_gg2")
    async def remote_bypass_gg2(self, logical_address, value):
        """
        :param data: Dictionary, {"address": 1-40, "value": False or True}
        :return:
        """
        index = logical_address - 1
        address = 0x527 + index // 16
        bit = index % 16
        await self.write_bit(address, bit, value)
        await self.wait_on_bit(address, bit, check_to=value, timeout=2)

    @events.subscribe(topic="remote_bypass_rts")
    async def remote_bypass_rts(self, logical_address, value):
        """
        :param data: Dictionary, {"address": 1-12, "value": False or True}
        :return:
        """
        await self.write_bit(0x52A, logical_address - 1, value)
        await self.wait_on_bit(0x52A, logical_address - 1, check_to=value, timeout=2)

    @events.subscribe(topic="plc_trip_reset")
    async def plc_trip_reset(self):
        await self.write_bit(0x526, 15, 0)
        # Sleep for 500ms
        await asyncio.sleep(0.500)
        await self.write_bit(0x526, 15, 1)

    @events.subscribe(topic="trip_reset")
    async def trip_reset(self):
        await self.write(0x52C, 0)
        # Sleep for 500ms
        await asyncio.sleep(0.500)
        await self.write(0x52C, 0xA5)

    @staticmethod
    def parse_status(value):
        status: ModuleStatusBits = ModuleStatusBits(value & 0x7F)
        if status & (ModuleStatusBits.L1_CLASH | ModuleStatusBits.L2_CLASH):
            return ModuleStatus.CLASH
        elif status & ModuleStatusBits.SYSTEM_OWNED:
            return ModuleStatus.SYSTEM
        elif all(
            (
                status & ModuleStatusBits.GLOBAL_SELECT,
                status & ModuleStatusBits.L1_OWNED,
            )
        ):
            return ModuleStatus.L1_OWNED
        elif all(
            (
                status & ModuleStatusBits.GLOBAL_SELECT,
                status & ModuleStatusBits.L2_OWNED,
            )
        ):
            return ModuleStatus.L2_OWNED
        elif all(
            (status & ModuleStatusBits.ON_SCAN, status & ModuleStatusBits.L1_OWNED)
        ):
            return ModuleStatus.ONLINE
        elif all(
            (
                status & ModuleStatusBits.ON_SCAN,
                not (status & ModuleStatusBits.L1_OWNED),
            )
        ):
            return ModuleStatus.OFFLINE
        elif not (status & ModuleStatusBits.ON_SCAN):
            return ModuleStatus.NEVER_ONLINE
        else:
            return ModuleStatus.UNKNOWN

    @events.subscribe(topic="imac_module_status")
    async def process_module_status_diff(self, data, timestamp):
        try:
            diff = {
                index: status
                for index, status in enumerate(data["address-status"])
                if status != self.current_state["address-status"][index]
            }
            if diff:
                self.current_state.update(data)
                events.publish(
                    "imac_discover_addresses", data=diff, timestamp=timestamp
                )
        except KeyError:
            # This is the first read, discover the full system
            self.current_state.update(data)
            events.publish("imac_discover_system")
        events.publish("imac_controller_data", data=data, timestamp=timestamp)

    @events.subscribe(topic="imac_discover_system")
    async def auto_discover_system(self):
        """
        Does a full system roll coll
        :return:
        """
        async with self.auto_discover_lock:
            online_addresses = {
                address
                for address, status in enumerate(self.current_state["address-status"])
                if status in {ModuleStatus.ONLINE}
            }
            # Check for RTSs based on schema
            for address in online_addresses:
                schema = self.address_schema_match(address)
                if "rts-config-0" == schema["name"]:
                    # TODO This could race against the poll pipeline for having master-fieldbus-number
                    rts_number = address - schema["range"][0] + 1
                    dev_id = f"RTS-{self.current_state['master-fieldbus-number']}-{rts_number}"
                    mod = {
                        "dev_id": dev_id,
                        "imac_address": address,
                        "module_type": "rts",
                    }
                    log.info(f"Roll call System: {mod}")
                    await self.update_devices([mod])

            async for roll_module in self.roll_call():
                # Find the discovered devices
                mod = self.decode_roll_call_single(roll_module)
                log.info(f"Roll call System: {mod}")
                await self.update_devices([mod])

    @events.subscribe(topic="imac_discover_addresses")
    async def auto_discover_modules(self, data, **kwargs):
        """
        Auto discovers modules based on the address status.
        Gets the devices to roll call based on address status.
        Failed roll calls are repeated with the auto discover lock still held.
        Devices that are returned are queried for their other addresses and removed from the roll call queue if the
        address is not clashed
        :param data:
        :param kwargs:
        :return:
        """
        async with self.auto_discover_lock:
            online_queue = {
                address
                for address, status in data.items()
                if status == ModuleStatus.ONLINE or address == 0
            }
            clash_queue = {
                address
                for address, status in data.items()
                if status == ModuleStatus.CLASH
            }
            system_queue = {
                address
                for address, status in data.items()
                if status in {ModuleStatus.SYSTEM, ModuleStatus.SYSTEM_ONLINE}
            }

            while True:
                if online_queue:
                    address = min(online_queue)
                elif clash_queue:
                    address = min(clash_queue)
                elif system_queue:
                    address = min(system_queue)
                else:
                    break
                addresses = {address}
                try:
                    async for imac_mod in self.discover_at_address(address):
                        # Find the discovered devices
                        await imac_mod.find_missing_starting_data()
                        addresses.update(imac_mod.identify_addresses().values())
                except asyncio.CancelledError:
                    log.info("Shutting down autodiscover")
                    return
                except BaseException as e:
                    if pyaware.evt_stop.is_set():
                        log.info("Shutting down autodiscover")
                        return
                    log.exception(e)
                    await asyncio.sleep(1)

                clash_queue.discard(address)
                system_queue.discard(address)
                # Pop the discovered addresses from the online queue as we already know what is at those addresses
                online_queue.difference_update(addresses)

    async def discover_at_address(self, address):
        async for roll_module in self.roll_call_force(address):
            mod = self.decode_roll_call_single(roll_module)
            log.info(f"Roll call: Address: {address}, {mod}")
            await self.update_devices([mod])
            yield self.devices[mod["dev_id"]]
        # Check for RTSs based on schema
        schema = self.address_schema_match(address)
        if "rts-config" in schema["name"]:
            # Note we are creating RTSs even if there is a schema violation because we aren't kicking off
            # modules
            # TODO This could race against the poll pipeline for having master-fieldbus-number
            rts_number = address - schema["range"][0] + 1
            dev_id = f"RTS-{self.current_state['master-fieldbus-number']}-{rts_number}"
            mod = {"dev_id": dev_id, "imac_address": address, "module_type": "rts"}
            log.info(f"Roll call: Address: {address}, {mod}")
            await self.update_devices([mod])
            yield self.devices[mod["dev_id"]]

    def address_schema_violation(
        self, address, imac_module_roll: typing.List[dict]
    ) -> list:
        """
        Checks the loaded schema to determine if a address violation has occured
        :param address:
        :param imac_module_roll:
        :return:
        """
        schema = self.address_schema_match(address)
        violations = []
        for imac_module in imac_module_roll:
            # Enforce schema
            if self._address_schema_violation(schema, imac_module):
                log.info(
                    f"Schema Violation: Address: {address}, {imac_module['dev_id']}:"
                    f"{imac_module['module_type']}"
                )
                violations.append(imac_module)
        return violations

    def _address_schema_violation(self, schema, imac_module_roll: dict) -> bool:
        if schema.get("allowed_modules") is not None:
            return imac_module_roll["module_type"] not in schema["allowed_modules"]
        return False

    def address_status_schema_violation(self, address, status: ModuleStatus) -> bool:
        """
        Checks the loaded schema to determine if a address violation has occured
        :param address:
        :param imac_module_roll:
        :return:
        """
        schema = self.address_schema_match(address)
        if schema.get("allowed_statuses") is not None:
            return status.name not in schema["allowed_statuses"]
        return False

    def address_schema_match(self, address) -> dict:
        for schema in self.schema.get("address", []):
            if address in range(*schema["range"]):
                return schema

    def address_schema_match_by_name(self, name) -> dict:
        for schema in self.schema.get("address", []):
            if schema.get("name") == name:
                return schema
        raise ValueError("No Schema Match")

    @events.subscribe(topic="clear_address")
    async def clear_status_at_address(self, data):
        await self.write_bit(data + 0x100, 0, 0)

    def remove_device_from_schedule(self, dev_id: str):
        remove_items = {k for k in self.schedule_reads if k.split("::")[0] == dev_id}
        for k in remove_items:
            del self.schedule_reads[k]

    def update_store_state(self, parameters: dict):
        """
        Update the state the module has represented in the cache database
        :param parameters: Parameter dictionary to update the state
        :return:
        """
        self.store_state.update(parameters)

    def update_send_state(self, parameters: dict):
        """
        Update the state used the module has represented from queued mqtt messages
        :param parameters: Parameter dictionary to update the state
        :return:
        """
        self.send_state.update(parameters)

    def update_event_state(self, parameters: dict):
        """
        Update the state used the module has represented from queued mqtt messages
        :param parameters: Parameter dictionary to update the state
        :return:
        """
        self.event_state.update(parameters)

    def update_current_state(self, parameters: dict):
        """
        Update the state used to run diff module data against
        :param parameters: Parameter dictionary to update the state
        :return:
        """
        self.current_state.update(parameters)

    @events.subscribe(topic="sync_rtc")
    async def rtc_sync(self, timestamp: int):
        """
        Writes to NVM 13 and 14 the timestamp for the real time clock
        This is Ampcontrol Epoch of 01/01/2000 with high byte in NVM 13 and low byte in NVM 14
        This will be an integer sent from the master which should have the necessary conversions to Ampcontrol Epoch
        already implemented.
        The timestamp is offset by the amount of time setting up so that the time written is closer to accurate.
        Note that there will be other time offsets due to communication times and loop and the fact that Ampcontrol
        Epoch has a resolution of seconds.
        :return:
        """
        start = time.time()
        await self.write(0x52D, 0, 0)
        await asyncio.sleep(3)
        values = struct.unpack(
            ">HH", struct.pack(">I", round(timestamp + time.time() - start))
        )
        await self.write(0x52D, *values)

    def identify(self):
        return self.dict()

    def dict(self):
        response = {"type": self.module_type}
        if self.current_state.get("serial-number"):
            response["serial"] = self.current_state.get("serial-number")
        return response
