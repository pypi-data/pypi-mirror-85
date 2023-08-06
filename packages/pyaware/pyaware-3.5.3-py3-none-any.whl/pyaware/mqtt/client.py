import datetime
import logging.handlers
import asyncio
import time
from collections import defaultdict
from pyaware import events, StopException
import hbmqtt.client
from hbmqtt.client import ClientException, ConnectException
from hbmqtt.mqtt.constants import QOS_1
from pyaware.mqtt import models, transformations, factories, log_to_file
from pyaware.store import disk_storage
import pyaware.config
import uuid
import typing
from dataclasses import dataclass, field

try:
    import rapidjson as json
except ImportError:
    import json

log = logging.getLogger(__file__)


@dataclass(order=True)
class MsgItem:
    priority: int
    topic: str
    payload: str
    uid: str
    qos: int
    fut: asyncio.Future = field(compare=False)


# Patch the client to handle reconnect logic
class MQTTClient(hbmqtt.client.MQTTClient):
    def __init__(self, client_id=None, config=None, loop=None):
        self._on_connect = None
        self.uri_gen = None
        self.disconnect_after = 0
        self._disconnect_after_task: typing.Optional[asyncio.Future] = None
        self._on_connect_task = None
        self.connect_params = {}
        super().__init__(client_id, config, loop)

    @property
    def on_connect(self):
        """If implemented, called when the broker responds to our connection
        request."""
        return self._on_connect

    @on_connect.setter
    def on_connect(self, func):
        """Define the connect callback implementation.

        Expected signature is:
            connect_callback()
        """
        self._on_connect = func

    @property
    def on_disconnect(self):
        """If implemented, called when the broker responds to our connection
        request."""
        return self._on_disconnect

    @on_disconnect.setter
    def on_disconnect(self, func):
        """Define the connect callback implementation.

        Expected signature is:
            connect_callback()
        """
        self._on_disconnect = func

    @asyncio.coroutine
    def connect(
        self,
        uri=None,
        cleansession=None,
        cafile=None,
        capath=None,
        cadata=None,
        extra_headers=None,
    ):
        if extra_headers is None:
            extra_headers = {}
        self.extra_headers = extra_headers
        self.connect_params = {
            "uri": uri,
            "cleansession": cleansession,
            "cafile": cafile,
            "capath": capath,
            "cadata": cadata,
        }
        try:
            return (yield from self._do_connect())
        except BaseException as be:
            self.logger.warning("Connection failed: %r" % be)
            auto_reconnect = self.config.get("auto_reconnect", False)
            if not auto_reconnect:
                raise
            else:
                return (yield from self.reconnect())

    @asyncio.coroutine
    def _do_connect(self):
        if self.uri_gen:
            uri = self.uri_gen()
        else:
            uri = self.connect_params["uri"]
        cleansession = self.connect_params["cleansession"]
        cafile = self.connect_params["cafile"]
        capath = self.connect_params["capath"]
        cadata = self.connect_params["cadata"]
        self.session = self._initsession(uri, cleansession, cafile, capath, cadata)
        return_code = yield from self._connect_coro()
        self._disconnect_task = asyncio.ensure_future(
            self.handle_connection_close(), loop=self._loop
        )
        if self.disconnect_after:

            async def disconnect_later():
                """
                Starts the disconnect procedure after a set number of seconds
                Keeps the handle_connection_close intact so that the reconnect logic still
                works
                :return:
                """
                await asyncio.sleep(self.disconnect_after)
                log.warning("Scheduled mqtt disconnect")
                if self.session.transitions.is_connected():
                    await self._handler.mqtt_disconnect()
                else:
                    self.logger.warning(
                        "Client session is not currently connected, ignoring scheduled disconnect"
                    )

            self._disconnect_after_task = asyncio.ensure_future(
                disconnect_later(), loop=self._loop
            )
        if return_code == 0 and self.on_connect:
            self._on_connect_task = asyncio.ensure_future(
                self.on_connect(), loop=self._loop
            )
        return return_code

    async def handle_connection_close(self):
        def cancel_tasks():
            self._no_more_connections.set()
            while self.client_tasks:
                task = self.client_tasks.popleft()
                if not task.done():
                    task.set_exception(ClientException("Connection lost"))

        self.logger.debug("Watch broker disconnection")
        # Wait for disconnection from broker (like connection lost)
        await self._handler.wait_disconnect()
        self.logger.warning("Disconnected from broker")
        if self._disconnect_after_task:
            if not self._disconnect_after_task.done():
                self._disconnect_after_task.cancel()
        if self.on_disconnect:
            try:
                self.on_disconnect()
            except asyncio.CancelledError:
                raise
            except BaseException as e:
                log.error(e)

        # Block client API
        self._connected_state.clear()

        # stop an clean handler
        self._handler.detach()
        self.session.transitions.disconnect()

        if self.config.get("auto_reconnect", False):
            # Try reconnection
            self.logger.debug("Auto-reconnecting")
            try:
                await self.reconnect()
            except ConnectException:
                # Cancel client pending tasks
                cancel_tasks()
        else:
            # Cancel client pending tasks
            cancel_tasks()


@events.enable
class Mqtt:
    """
    Class for setting up google mqtt protocol.
    Assumes that Key Certificates are already generated and the device is created with the associated public key
    """

    def __init__(self, config, gateway_config: dict = None, _async: bool = False):
        """
        :param config: Config dictionary. Must have at least the device_id specified
        """
        self.config = config
        self.gateway_config = gateway_config or {}
        self.mqtt_promises = {}
        self.cmds_active = set([])
        self.client = MQTTClient(
            self.config.client_id,
            config={
                "default_qos": self.config.publish_qos,
                "auto_reconnect": True,
                "reconnect_max_interval": 60,
                "reconnect_retries": -1,
                "keep_alive": self.config.keepalive,
            },
        )
        self.client.uri_gen = self.gen_uri
        if self.config.token_life > 1:
            self.client.disconnect_after = self.config.token_life * 60 - 60
        else:
            self.client.disconnect_after = 0
        self.client.on_connect = self.setup
        self.client.on_disconnect = self.clean_up
        self.topic_loggers = {}
        self.log_messages = True
        self.sub_handles = {}
        self.active_uids = set([])
        self.message_queues = defaultdict(
            lambda: asyncio.PriorityQueue(self.config.max_message_queue_size)
        )
        if self.config.batch:
            self.message_manager = MessageManagerBatch(
                self.publish,
                self.config.max_message_queue_size,
                self.config.batch_hold_off,
            )
        else:
            self.message_manager = MessageManagerSingle(
                self.publish, self.config.max_message_queue_size
            )
        self.backlog_manager = BacklogManager(self.message_manager.evt_setup)
        asyncio.create_task(self.message_manager.start())
        asyncio.create_task(self.backlog_manager.start(self.message_manager.add))

    async def setup(self):
        # self.message_manager.clear()
        while True:
            if pyaware.evt_stop.is_set():
                raise StopException("Pyaware is stopped")
            try:
                await self._setup()
                log.info(f"Setup gateway mqtt {self.config.device_id}")
                break
            except (asyncio.CancelledError, StopException, GeneratorExit):
                raise
            except BaseException as e:
                log.exception(e)
            await asyncio.sleep(1)

    async def _setup(self):
        """
        Get config if it exists. Then set up attached devices from the config
        :return:
        """
        try:
            device_attaches = [
                self.publish(
                    self.config.parsers["attach"]["topic"].format(device_id=device_id),
                    json.dumps({"authorization": ""}),
                    qos=QOS_1,
                )
                for device_id in self.gateway_config.get("devices", [])
            ]
            await asyncio.gather(*device_attaches)
        except KeyError:
            pass
        sub_topics = [
            (
                self.config.parsers["config"]["topic"].format(
                    device_id=self.config.device_id
                ),
                1,
            ),
            (
                self.config.parsers["errors"]["topic"].format(
                    device_id=self.config.device_id
                ),
                0,
            ),
            (
                self.config.parsers["commands"]["topic"].format(
                    device_id=self.config.device_id
                ),
                0,
            ),
        ]
        sub_topics.extend(
            [
                (self.config.parsers["config"]["topic"].format(device_id=device_id), 1)
                for device_id in self.gateway_config.get("devices", [])
            ]
        )
        sub_topics.extend(
            [
                (self.config.parsers["errors"]["topic"].format(device_id=device_id), 0)
                for device_id in self.gateway_config.get("devices", [])
            ]
        )
        sub_topics.extend(
            [
                (
                    self.config.parsers["commands"]["topic"].format(
                        device_id=device_id
                    ),
                    0,
                )
                for device_id in self.gateway_config.get("devices", [])
            ]
        )
        self.sub_handles = [
            (f"config", self.handle_config),
            (f"errors", self.handle_errors),
            (f"commands/system/stop", self.handle_stop),
            (f"commands", self.handle_commands),
        ]
        await self.client.subscribe(sub_topics)
        self.message_manager.evt_setup.set()

    def clean_up(self):
        self.message_manager.clear()

    async def connect(self):
        if self.config.authentication_required:
            await self.client.connect(
                uri=None,
                cleansession=self.config.clean_session,
                cafile=self.config.ca_certs_path,
            )
        else:
            await self.client.connect(
                uri=f"mqtt://{self.config.host}:{self.config.port}",
                cleansession=self.config.clean_session,
            )

    def gen_uri(self):
        if self.config.authentication_required:
            return f"mqtts://unused:{self.config.jwt_token.decode('utf-8')}@{self.config.host}:{self.config.port}"
        else:
            return f"mqtt://{self.config.host}:{self.config.port}"

    async def loop(self):
        while True:
            if pyaware.evt_stop.is_set():
                log.info(
                    f"Stopping event loop for hbmqtt client {self.config.device_id}"
                )
                break
            try:
                msg = await self.client.deliver_message(timeout=1)
            except asyncio.TimeoutError:
                continue
            except (AttributeError, IndexError):
                await asyncio.sleep(1)
                continue
            except asyncio.CancelledError:
                raise
            except BaseException as e:
                log.exception(e)
                continue
            asyncio.get_event_loop().run_in_executor(None, self.sub_handler, msg)
            log.info("Message Received")

    def sub_handler(self, msg):
        for handle_str, handle in self.sub_handles:
            if handle_str in msg.topic:
                try:
                    if handle is not None:
                        handle(msg)
                        break
                except asyncio.CancelledError:
                    raise
                except BaseException as e:
                    log.exception(e)

    @events.subscribe(topic=f"trigger_send/#", parse_topic=True)
    async def send(self, *, data: dict, topic_type: str, topic: str, **kwargs):
        if topic_type not in self.config.parsers:
            return
        sub_topic = topic
        device_id = sub_topic.split("trigger_send/")[-1]
        uid = str(uuid.uuid4())
        delay = 2 + self.config.batch_hold_off
        payload, topic = self.form_message(
            data=data, topic_type=topic_type, uid=uid, **kwargs
        )
        topic = topic.format(device_id=device_id)
        fut = disk_storage.mqtt.insert_delayed(
            topic, payload, self.config.publish_qos, uid=uid, delay=delay
        )
        await self.message_manager.add(
            topic, payload, uid, self.config.publish_qos, fut, priority=0
        )

    async def publish(
        self,
        topic,
        payload,
        qos,
    ):
        """
        Publish a message to the mqtt broker
        This will first queue up a store the message cache on a delay of 2 seconds. If the message isn't acknowledged
        within 2 seconds, then the message will be stored in cache.
        If the message is finally acknowledged then the cache will have the message marked as ack'd.
        :param topic:
        :param payload:
        :param qos:
        :return:
        """
        try:
            payload = payload.encode()
        except AttributeError:
            pass
        await self.client.publish(topic, payload, qos)

    def form_message(
        self, data: dict, topic_type: str, **kwargs
    ) -> typing.Tuple[str, str]:
        parsers = self.config.parsers.get(topic_type, {})
        factory = factories.get_factory(parsers.get("factory"))
        msg = factory(data=data, **kwargs)
        for transform in parsers.get("transforms", []):
            msg = transformations.get_transform(**transform)(msg)
        msg = models.model_to_json(parsers.get("model", {}), msg)
        topic = parsers.get("topic", "")
        return msg, topic

    def mqtt_log(self, topic, payload, mid, resolved=False):
        if log_to_file:
            try:
                mqtt_log = self.topic_loggers[topic]
            except KeyError:
                mqtt_log = logging.getLogger(topic)
                mqtt_log.setLevel(logging.INFO)
                log_dir = pyaware.config.aware_path / "mqtt_log"
                log_dir.mkdir(parents=True, exist_ok=True)
                formatter = logging.Formatter("%(asctime)-15s %(message)s")
                handler = logging.handlers.TimedRotatingFileHandler(
                    log_dir / f"{topic.replace('/', '_')}.log", "h", backupCount=2
                )
                handler.setFormatter(formatter)
                mqtt_log.addHandler(handler)
                mqtt_log.propagate = False
                self.topic_loggers[topic] = mqtt_log
            if resolved:
                mqtt_log.info(f"Resolved {self.config.host} {mid}")
                return
            mqtt_log.info(f"Publishing {self.config.host} {mid}:\n{payload}")

    async def subscribe(self, topic, callback, qos):
        await self.client.subscribe([(topic, qos)])
        self.sub_handles[topic] = callback

    async def unsubscribe(self, topic):
        if self.client._connected_state.is_set():
            await self.client.unsubscribe([topic])
            self.sub_handles.pop(topic, None)

    def handle_config(self, msg):
        """
        If the gateway handle config to update devices and set up remaining pyaware config
        :return:
        """
        if msg.topic == f"/devices/{self.config.device_id}/config":
            """
            Check if new config is different to the old config
            If so, override config cache present and restart pyaware cleanly
            """
            log.info("Gateway config received: {}".format(msg.data))
            if msg.data:
                new_config_raw = msg.data.decode()
                if new_config_raw != pyaware.config.load_config_raw(
                    pyaware.config.config_main_path
                ):
                    pyaware.config.save_config_raw(
                        pyaware.config.config_main_path, new_config_raw
                    )
                    log.warning("New gateway configuration detected. Stopping process")
                    pyaware.stop()
        else:
            log.info(f"Device config {msg.topic} received: {msg.data}")

    def handle_errors(self, mid):
        try:
            log.warning(f"Error received from gcp\n{mid.data.decode('utf-8')}")
        except:
            log.warning(f"Error received from gcp\n{mid.data}")

    def handle_commands(self, mid):
        try:
            msg = json.loads(mid.data)
        except AttributeError:
            # Ignore commands with no payload
            return
        except json.JSONDecodeError as e:
            log.exception(e)
            return
        self.cmds_active.add(msg["id"])
        pyaware.events.publish(
            f"mqtt_command/{self.config.device_id}",
            data=msg,
            timestamp=datetime.datetime.utcnow(),
        )

    def handle_stop(self, mid):
        pyaware.stop()

    # TODO this needs to have a instance ID as any more than one MQTT device will break here (eg. 2 imacs)
    @events.subscribe(topic=f"mqtt_command_response/#", parse_topic=True)
    async def publish_command_response(
        self, data: dict, timestamp: datetime.datetime, topic: str
    ):
        await self.send(
            data=data,
            topic_type="command_response",
            topic=f"trigger_send/{topic.split('/')[1]}",
            timestamp=timestamp,
        )
        if data["type"] > 1:
            self.cmds_active.discard(data["id"])


class MessageManager:
    def __init__(
        self,
        publish_cbf: typing.Callable,
        max_queue_size: int = 0,
        max_in_flight_messages: int = 100,
    ):
        self.evt_setup = asyncio.Event()
        self.publish = publish_cbf
        self.max_queue_size = max_queue_size
        self.in_flight: dict = {}
        self.sem_in_flight = asyncio.BoundedSemaphore(max_in_flight_messages)
        self.max_in_flight_messages = max_in_flight_messages

    async def handle_publish_flow(
        self,
        topic,
        payload,
        qos: int,
        futs: typing.List[typing.Tuple[str, asyncio.Future]],
    ):
        """
        Handles the publish flow for storing the
        :param topic:
        :param payload:
        :param qos:
        :param futs: Contains the uid, future pairing to mark a message as complete.
        The fut is an asyncio.Future which is the task that commits the mqtt message to disk after a set time.
        As messages can be batches, they can contain multiple uids for a single message send.
        The database commit futures are cancelled if the message is successfully received by the broker before being
        committed to the database
        :param sem: A semaphore that needs to be released when the message has finished processing either by success or
        error
        :return:
        """
        try:
            await asyncio.wait_for(self.evt_setup.wait(), 10)
            await asyncio.wait_for(
                self.publish(topic, payload, qos=qos),
                10,
            )
            for uid, fut in futs:
                if fut.done():
                    asyncio.create_task(disk_storage.mqtt.ack(uid))
                else:
                    fut.cancel()
        except (asyncio.TimeoutError, asyncio.CancelledError):
            pass
        finally:
            for uid, fut in futs:
                self.in_flight.pop(uid, None)
            self.sem_in_flight.release()

    def clear(self):
        log.info("Cleaning up in flight messages")
        self.evt_setup.clear()
        for task in set(self.in_flight.values()):
            try:
                task.cancel()
            except AttributeError:
                continue

    async def add(self, topic, payload, uid, qos, fut, priority: int = 0):
        raise NotImplementedError

    async def start(self):
        raise NotImplementedError


class MessageManagerBatch(MessageManager):
    def __init__(
        self,
        publish_cbf: typing.Callable,
        max_queue_size: int = 0,
        batch_hold_off: int = 0,
        max_in_flight_messages: int = 100,
    ):
        super().__init__(publish_cbf, max_queue_size, max_in_flight_messages)
        self.batch_hold_off = batch_hold_off
        self.queues = {}

    async def add(self, topic, payload, uid, qos, fut, priority: int = 0):
        if uid in self.in_flight:
            return
        self.in_flight[uid] = None
        if topic not in self.queues:
            self.queues[topic] = asyncio.PriorityQueue(self.max_queue_size)
            asyncio.create_task(self._start(self.queues[topic]))
        await self.queues[topic].put(MsgItem(priority, topic, payload, uid, qos, fut))

    async def start(self):
        """
        This function doesn't need to be called because there is a task for each queue created on a new topic addition
        in the add method
        :return:
        """

    async def _start(self, q):
        """
        Group messages by topic
        Uses the publish qos by default
        :return:
        """
        start = time.time()
        while True:
            msg = await self._pull_from_queue(q)
            if msg:
                await self.sem_in_flight.acquire()
                task = asyncio.create_task(self.handle_publish_flow(**msg))
                for uid, fut in msg["futs"]:
                    self.in_flight[uid] = task
                    q.task_done()
                sleep_time = 0.1
                start = time.time()
            else:
                sleep_time = time.time() - start + self.batch_hold_off
                start = time.time()
                if sleep_time < 0.1:
                    sleep_time = 0.1
            await asyncio.sleep(sleep_time)

    async def _pull_from_queue(self, q) -> dict:
        payloads = []
        futs = []
        max_qos = 0
        msg = None
        while True:
            try:
                msg = q.get_nowait()
                payloads.append(msg.payload)
                futs.append((msg.uid, msg.fut))
                max_qos = max(max_qos, msg.qos)
            except asyncio.QueueEmpty:
                break
        if not msg:
            return {}
        return {
            "topic": msg.topic,
            "payload": f"[{','.join(payloads)}]",
            "qos": max_qos,
            "futs": futs,
        }


class MessageManagerSingle(MessageManager):
    def __init__(
        self,
        publish_cbf: typing.Callable,
        max_queue_size: int = 0,
        max_in_flight_messages: int = 1000,
    ):
        super().__init__(publish_cbf, max_queue_size, max_in_flight_messages)
        self.q = asyncio.PriorityQueue(max_queue_size)

    async def add(self, topic, payload, uid, qos, fut, priority: int = 0):
        if uid in self.in_flight:
            return
        self.in_flight[uid] = None
        await self.q.put(MsgItem(priority, topic, payload, uid, qos, fut))

    async def start(self):
        while True:
            msg = await self.q.get()
            await self.sem_in_flight.acquire()
            self.in_flight[msg.uid] = asyncio.create_task(
                self.handle_publish_flow(
                    msg.topic,
                    msg.payload,
                    msg.qos,
                    [(msg.uid, msg.fut)],
                )
            )
            self.q.task_done()


class BacklogManager:
    def __init__(self, evt_setup: asyncio.Event):
        self.evt_setup = evt_setup

    async def start(
        self,
        a_callback: typing.Union[MessageManagerBatch.add, MessageManagerSingle.add],
    ):
        """
        Continually add messages the the queue from the disk storage if they are not currently in flight
        :param a_callback: Callback to the message manager.
        Will block adding messages if the manager queue is full
        :return:
        """
        log.info(f"Starting mqtt backlog")
        while True:
            start = time.time()
            if pyaware.evt_stop.is_set():
                log.info("Shutting down mqtt backlog manager")
                return
            msg_cnt = 0
            try:
                async for row in disk_storage.mqtt.get_all_unsent(1000):
                    await self.evt_setup.wait()
                    fut = asyncio.Future()
                    # Indicate that the data is already committed to disk
                    fut.set_result(None)
                    await a_callback(**row, fut=fut, priority=1)
                    msg_cnt += 1
                if msg_cnt > 0:
                    log.info(
                        f"Finished adding mqtt backlog for {msg_cnt} in {time.time() - start}s"
                    )
            except asyncio.CancelledError:
                if pyaware.evt_stop.is_set():
                    log.info("Shutting down mqtt backlog manager")
                    return
            except asyncio.InvalidStateError:
                log.info(
                    "aiosqlite race condition error see https://github.com/omnilib/aiosqlite/issues/80"
                )
            except BaseException as e:
                log.error(e)
            await asyncio.sleep(60)
