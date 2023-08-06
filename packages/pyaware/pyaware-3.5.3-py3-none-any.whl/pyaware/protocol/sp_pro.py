import asyncio
import struct
from datetime import datetime

import pyaware
import pyaware.data_types
import pyaware.triggers
import pyaware.aggregations
import pyaware.transformations
from pyaware.store import storage
from pyaware import events
from pyaware import log
from pyaware.mqtt.models import TopologyChildrenV2

from aiosppro.serial import SPPROSerialClient


class SPPRODevice:
    dev_type = "sppro-device"

    def __init__(self, client: SPPROSerialClient, device_id: str, config):
        self.client = client
        self.device_id = device_id
        self.store_state = {}
        self.send_state = {}
        self.event_state = {}
        self.current_state = {}
        self.config = pyaware.config.load_config(config)
        self.parameters = pyaware.data_types.parse_data_types(
            self.config["parameters"], {}
        )
        self.triggers = pyaware.triggers.build_from_device_config(
            config,
            device_id=device_id,
            send_state=self.send_state,
            store_state=self.store_state,
            event_state=self.event_state,
            current_state=self.current_state,
        )
        self.transformations = pyaware.transformations.build_from_device_config(config)
        self.aggregates = pyaware.aggregations.build_from_device_config(config)
        for name, source_config in self.config["sources"].items():
            if source_config.get("type", "poll") == "poll":
                try:
                    self.poll_interval = self.config["sources"][name]["poll_interval"]
                except KeyError:
                    self.poll_interval = 5
                asyncio.create_task(self.trigger_poll(name))

    async def trigger_poll(self, source: str):
        loop = asyncio.get_running_loop()
        start = loop.time()
        log.info(f"Waiting for connection for {self.device_id}")
        await self.client.connected.wait()
        log.info(f"Starting poll pipeline for {self.device_id}")
        blocks = self.config["sources"][source]["blocks"]
        while True:
            if pyaware.evt_stop.is_set():
                log.info(f"Closing SP PRO device {self.device_id} polling")
                return
            try:
                start = loop.time()
                await self.poll_pipeline(blocks, source)
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning(
                        f"SP PRO device {self.device_id} cancelled without stop signal"
                    )
                    continue
            except BaseException as e:
                if not pyaware.evt_stop.is_set():
                    log.exception(e)
            sleep_time = start - loop.time() + self.poll_interval
            if sleep_time > 0:
                await asyncio.sleep(start - loop.time() + self.poll_interval)

    async def poll_pipeline(self, blocks, source):
        addr_map = pyaware.data_types.AddressMapUint16()
        for start, end in blocks:
            count = len(range(start, end))
            addr_map.merge(await self.read(start, count))
        timestamp = datetime.utcnow()
        if timestamp is None:
            timestamp = datetime.utcnow()
        device_data = {}
        for k, v in self.config["parameters"].items():
            if v.get("source") == source:
                try:
                    device_data.update(self.parameters[k].decode(addr_map))
                except KeyError:
                    pass
        processed_data = await self.process_data(device_data, timestamp)
        self.current_state.update(device_data)

    async def process_data(self, data, timestamp):
        transformed_data = pyaware.transformations.transform(data, self.transformations)
        store_data, send_data, event_data = await asyncio.gather(
            pyaware.triggers.process.run_triggers(
                self.triggers.get("process", {}).get("store", []),
                transformed_data,
                timestamp,
            ),
            pyaware.triggers.process.run_triggers(
                self.triggers.get("process", {}).get("send", []),
                transformed_data,
                timestamp,
            ),
            pyaware.triggers.process.run_triggers(
                self.triggers.get("process", {}).get("event", []),
                transformed_data,
                timestamp,
            ),
        )
        if store_data:
            storage.update(store_data, topic=f"{self.device_id}")
            self.store_state.update(store_data)
        if send_data:
            storage.update(send_data, topic=f"{self.device_id}")
            cached_data = storage.pop(f"{self.device_id}")
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
            self.send_state.update(cached_data)
        if event_data:
            for param, value in event_data.items():
                events.publish(
                    f"parameter_trigger/{self.device_id}/{param}",
                    data=next(iter(value.values())),
                    timestamp=timestamp,
                )
            self.event_state.update(event_data)
        return send_data

    async def read(self, start_addr: int, num_addr_to_read: int, timeout=None):
        addr_map = pyaware.data_types.AddressMapUint16()
        data = await self.client.read(
            start_addr=start_addr, num_addr_to_read=num_addr_to_read, timeout=timeout
        )
        try:
            # Expecting 16-bit word for each address, so unpacking as such and capturing the rest.
            # returns empty data if data cannot be unpacked.
            unpacked_data = struct.unpack("<" + "H" * (len(data) // 2), data)
            addr_map[start_addr : start_addr + num_addr_to_read] = unpacked_data
        except (struct.error, IndexError) as e:
            log.exception(e)
            log.warning(
                f"SP PRO device {self.device_id} data was unpacked improperly or set improperly into the address map."
                f"Expecting 16-bit word for each address. Data received: {data}"
            )
        return addr_map

    def identify(self):
        response = TopologyChildrenV2(
            values={},
            type=self.dev_type,
            serial=self.device_id,
            children=[],
        )
        return response

    def dict(self):
        response = {"type": self.dev_type}
        return response
