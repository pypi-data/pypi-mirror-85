import yaml
from flask import current_app

from raspcuterie import base_path
from raspcuterie.devices import InputDevice
from raspcuterie.devices.control import ControlRule
from raspcuterie.devices.output.relay import OutputDevice


def parse_config(config_name="config.yaml"):

    file = base_path / config_name

    InputDevice.discover()
    OutputDevice.discover()

    with file.open() as f:
        data_loaded = yaml.safe_load(f)

        return data_loaded


def register_input_devices(config):

    input_devices = config["devices"]["input"]

    for device_name, device in input_devices.items():

        device_type = device.get("type", device_name)

        if device_type in InputDevice.types:
            device_class = InputDevice.types[device_type]
            device_class(device_name)
        else:
            current_app.logger.error(f"Cloud not initiate {device}")


def register_output_devices(config):

    input_devices = config["devices"]["output"]

    for device_name, device in input_devices.items():

        device_type = device.get("type", device_name)

        device_class = OutputDevice.types[device_type]

        kwargs = device.copy()

        del kwargs["type"]

        device_class(device_name, **kwargs)


def register_config_rules(config):

    control_rules = config["control"]

    for device, rules in control_rules.items():

        device = OutputDevice.registry[device]

        for rule in rules:

            ControlRule(
                device,
                expression=rule["expression"],
                action=rule["action"],
                name=rule["rule"],
            )


def setup(app):
    if app.debug or app.testing:
        config = parse_config("config_dev.yaml")
    else:
        config = parse_config()
    register_input_devices(config)
    register_output_devices(config)
    register_config_rules(config)
