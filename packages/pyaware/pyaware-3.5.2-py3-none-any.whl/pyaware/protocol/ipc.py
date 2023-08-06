import platform
import asyncio
import logging
import pyaware
from pyaware.protocol.imac2.protocol import Imac2Protocol
from typing import Union
from datetime import datetime
from dataclasses import dataclass
from pyaware.mqtt.models import TopologyV2, TopologyChildrenV2

from pyaware import events

log = logging.getLogger(__file__)


@events.enable
@dataclass
class GatewayIPC:
    eth_interface: str
    device_id: str
    main_device: Union[Imac2Protocol] = None
    ip_address: str = ""

    def __post_init__(self):
        self.devices = []
        self.identify()
        asyncio.create_task(self.send_gateway_heartbeat())
        asyncio.create_task(self.update_state())

    async def update_state(self):
        log.info("Starting gateway update state")
        version = pyaware.__version__
        state = self.identify()
        state.values["version"] = version
        events.publish(
            f"trigger_send/{self.device_id}",
            topic_type="state",
            data=state.values,
            timestamp=datetime.utcnow(),
        )

    async def send_gateway_heartbeat(self):
        log.info("Starting gateway heartbeat writes")
        while True:
            if pyaware.evt_stop.is_set():
                log.info("Closing gateway heartbeat")
                return
            try:
                await asyncio.sleep(5)
                ip_address = asyncio.create_task(self.fetch_ip())
                if await ip_address != self.ip_address:
                    self.ip_address = await ip_address
                    events.publish(
                        f"device_topology/{self.device_id}",
                        data={},
                        timestamp=datetime.utcnow(),
                    )
                    asyncio.create_task(self.update_state())
                timestamp = datetime.utcnow()
                data = {"ipAddress": await ip_address, "timestamp": timestamp}
                events.publish(
                    f"trigger_send/{self.device_id}",
                    data=data,
                    timestamp=timestamp,
                    topic_type="gateway_heartbeat",
                )
                await asyncio.sleep(25)
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning("Gateway heartbeat cancelled without stop signal")
                    continue
            except BaseException as e:
                if not pyaware.evt_stop.is_set():
                    log.exception(e)

    async def fetch_ip(self) -> str:
        if platform.system() == "Linux":
            cmd = f"/sbin/ifconfig {self.eth_interface} | grep -Eo 'inet (addr:)?([0-9]*[.]){{3}}[0-9]*' | grep -Eo '([0-9]*[.]){{3}}[0-9]*'"
            proc = await asyncio.create_subprocess_shell(
                cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            log.debug(
                f"Fetch IP Address Sent Request:[{cmd!r} exited with {proc.returncode}]"
            )
            if stdout:
                log.debug(f"IP Address Recieved: [stdout]\n{stdout.decode()}")
                ip_address = stdout.decode().rstrip()
                return ip_address
            if stderr:
                raise stderr
        else:
            # TODO: Add support for windows operating systems
            raise NotImplementedError(
                f"Current Operating System {platform.system()} is Unsupported"
            )

    def identify(self, child: TopologyChildrenV2 = None) -> TopologyV2:
        # TODO: Make device_id more explicit in config that it is a dynamic variable
        # TODO: Work out how to invalidate the cache when power is left on to IPC and the comms are swapped. IMAC use case.
        data = {}
        if self.main_device is not None:
            self.device_id = self.main_device.device_id
        if self.ip_address != "":
            data["ipAddress"] = self.ip_address
        if child is not None and child != {}:
            for index, device in enumerate(self.devices):
                if device.serial == child.serial:
                    self.devices[index] = child
                    return TopologyV2(
                        values=data, timestamp=datetime.utcnow(), children=self.devices
                    )
            self.devices.append(child)
        return TopologyV2(
            values=data, timestamp=datetime.utcnow(), children=self.devices
        )

    @events.subscribe(topic="device_topology/#")
    def update_topology(self, data, timestamp):
        payload = self.identify(child=data)
        log.info(f"New topology:  {payload}")
        events.publish(
            f"trigger_send/{self.device_id}",
            data=payload,
            timestamp=timestamp,
            topic_type="topology",
        )
