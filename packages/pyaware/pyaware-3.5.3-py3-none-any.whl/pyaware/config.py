"""
This module is intended to parse configuration files and instantiate the necessary systems within pyaware.
"""
from pkg_resources import parse_version
import ruamel.yaml
import logging
import pyaware
import pyaware.mqtt.config
import deepdiff
import asyncio
from functools import lru_cache
from pathlib import Path
from copy import deepcopy

aware_path = Path("")
config_main_path = Path("")

log = logging.getLogger(__file__)


@lru_cache()
def load_config_raw(file_path):
    with open(file_path) as f:
        return f.read()


@lru_cache()
def _load_config(file_path):
    try:
        with open(file_path) as f:
            return ruamel.yaml.safe_load(load_config_raw(file_path))
    except FileNotFoundError:
        with open(file_path, "w"):
            return {}


def load_config(file_path):
    """
    Load config in its raw form and produce a dictionary, raw
    :param file_path:
    :return: Loaded config, raw data
    """
    return deepcopy(_load_config(file_path))


def save_config(file_path, config):
    """
    Load config in its raw form and produce a dictionary, raw
    :param file_path:
    :return: Loaded config, raw data
    """
    with open(file_path, "w") as f:
        ruamel.yaml.dump(config, f, default_flow_style=False)
    _load_config.cache_clear()
    load_config_raw.cache_clear()


def save_config_raw(file_path, config):
    """
    Load config in its raw form and produce a dictionary, raw
    :param file_path:
    :return: Loaded config, raw data
    """
    with open(file_path, "w") as f:
        f.write(config)
    _load_config.cache_clear()
    load_config_raw.cache_clear()


class ConfigChanged(ValueError):
    pass


def config_changes(original, new):
    return deepdiff.DeepDiff(original, new, ignore_order=True)


def aware_version_check(config: dict):
    """
    Parse the gateway meta data to ensure that appropriate requirements are met
    :param config:
    :return:
    """
    # Check aware version
    if parse_version(pyaware.__version__) < parse_version(
        config["meta_data"]["aware_version"]
    ):
        # TODO self update in separate process and use older cached config (if existing) until update is complete
        # Then kill off process to let the new version start
        raise ValueError(
            "Currently installed pyaware version is not compatible with the config"
        )


def parse_modbus_rtu(port, **kwargs):
    """
    :param kwargs: All parameters required for instantiating the modbus client
    :return: Asyncronous modbus client
    """
    from pyaware.protocol.modbus import ModbusAsyncSerialClient

    client = ModbusAsyncSerialClient(port, **kwargs)
    return client


def parse_modbus_rtu2(port, **kwargs):
    """
    :param kwargs: All parameters required for instantiating the modbus client
    :return: Asyncronous modbus client
    """
    from aiomodbus.serial import ModbusSerialClient

    client = ModbusSerialClient(port, **kwargs)
    asyncio.get_event_loop().create_task(client.connect())
    return client


def parse_modbus_tcp(host, **kwargs):
    """
    :param kwargs: All parameters required for instantiating the modbus client
    :return: Partial function that can be called to initiate the object and connection.
    """
    from pyaware.protocol.modbus import ModbusAsyncTcpClient

    client = ModbusAsyncTcpClient(host, **kwargs)
    asyncio.get_event_loop().create_task(client.start())
    return client


def parse_modbus_tcp2(host, **kwargs):
    """
    :param kwargs: All parameters required for instantiating the modbus client
    :return: Partial function that can be called to initiate the object and connection.
    """
    from aiomodbus.tcp import ModbusTCPClient

    client = ModbusTCPClient(host, **kwargs)
    asyncio.get_event_loop().create_task(client.connect())
    return client


def parse_sp_pro(port: str, baudrate: int, parity: str, stopbits: int, **kwargs):
    from aiosppro.serial import SPPROSerialClient

    client = SPPROSerialClient(
        port=port, baudrate=baudrate, parity=parity, stopbits=stopbits, **kwargs
    )
    asyncio.get_event_loop().create_task(client.connect())
    return client


def parse_imac2_master(**kwargs):
    from pyaware.protocol.imac2.protocol import Imac2Protocol

    return Imac2Protocol(**kwargs)


def parse_modbus_device(**kwargs):
    from pyaware.protocol.modbus import ModbusDevice

    return ModbusDevice(**kwargs)


def parse_sp_pro_device(**kwargs):
    from pyaware.protocol.sp_pro import SPPRODevice

    return SPPRODevice(**kwargs)


def parse_hbmqtt_gcp(**kwargs):
    import pyaware.mqtt.client

    config = pyaware.config.load_config(aware_path / "config" / "cloud.yaml")
    config = pyaware.mqtt.config.GCPCloudConfig(**config, **kwargs)
    gateway_config = pyaware.config.load_config(aware_path / "config" / "gateway.yaml")
    client = pyaware.mqtt.client.Mqtt(config, gateway_config)
    asyncio.create_task(client.connect())
    asyncio.create_task(client.loop())
    return client


def parse_hbmqtt_raw(device_id, **kwargs):
    import uuid
    import pyaware.mqtt.client

    config = pyaware.mqtt.config.LocalConfig(str(uuid.uuid4()), device_id, **kwargs)
    gateway_config = pyaware.config.load_config(aware_path / "config" / "gateway.yaml")
    client = pyaware.mqtt.client.Mqtt(config, gateway_config)
    asyncio.create_task(client.connect())
    asyncio.create_task(client.loop())
    return client


def parse_gateway_ipc(**kwargs):
    from pyaware.protocol.ipc import GatewayIPC

    return GatewayIPC(**kwargs)


def parse_comm_params(comms, instances):
    comms_params = {}
    for (
        k,
        v,
    ) in comms["params"].items():
        if v["type"] == "value":
            comms_params[k] = v["value"]
        elif v["type"] == "ref_comms":
            comms_params[k] = instances[v["value"]]
        elif v["type"] == "ref_path":
            comms_params[k] = aware_path / Path(v["value"])
        elif v["type"] == "ref_device":
            comms_params[k] = (
                Path(pyaware.__file__).parent / "devices" / Path(v["value"])
            )
        else:
            raise ValueError("No valid type detected in config file")
    return comms_params


def parse_communication(communication: list):
    """
    :param communication:
    :return: dictionary of form
    {
      <id>:
        {
          "protocol": <string>, # eg. modbus_rtu, modbus_tcp
          "handler": handler to call to return the communication type in a connected state
        },
        {...},
      ...,
    }
    """
    protocol_handlers = {
        "modbus_rtu": parse_modbus_rtu,
        "modbus_rtu2": parse_modbus_rtu2,
        "modbus_tcp": parse_modbus_tcp,
        "modbus_tcp2": parse_modbus_tcp2,
        "sp_pro": parse_sp_pro,
        "imac2_gasguard_live": parse_imac2_master,
        "modbus_device": parse_modbus_device,
        "sp_pro_device": parse_sp_pro_device,
        "mqtt_raw": parse_hbmqtt_raw,
        "mqtt_gcp": parse_hbmqtt_gcp,
        "hbmqtt_raw": parse_hbmqtt_raw,
        "hbmqtt_gcp": parse_hbmqtt_gcp,
        "gateway_ipc": parse_gateway_ipc,
    }
    instances = {}
    for comms in communication:
        log.info(f"Initialising {comms['name']}")
        comms_params = parse_comm_params(comms, instances)
        instances[comms["name"]] = protocol_handlers[comms["type"]](**comms_params)
        log.info(f"Initialised {comms['name']}")
    return instances
