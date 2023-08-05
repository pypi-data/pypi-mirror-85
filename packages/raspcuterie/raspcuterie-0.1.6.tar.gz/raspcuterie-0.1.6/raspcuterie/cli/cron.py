import logging

from flask import current_app

from raspcuterie.cli import cli, with_appcontext
from raspcuterie.devices import InputDevice, OutputDevice
from raspcuterie.devices.control import ControlRule


def evaluate_config_rules():
    for rule in ControlRule.registry:
        rule.execute_if_matches()


@cli.command()
@with_appcontext
def log_values():
    current_app.logger.setLevel(logging.DEBUG)
    evaluate_config_rules()

    for input_device in InputDevice.registry.values():
        input_device.log()

    for output_device in OutputDevice.registry.values():
        output_device.log()


if __name__ == "__main__":
    log_values()
