from raspcuterie.devices.control import ControlRule
from raspcuterie.devices.output.relay import OutputDevice

from raspcuterie.config import (
    parse_config,
    register_input_devices,
    register_output_devices,
    register_config_rules,
)
from raspcuterie.devices import InputDevice


def test_parse_config():
    ControlRule.registry = []

    x = parse_config()

    assert x

    register_input_devices(x)

    assert len(InputDevice.registry) == 2

    register_output_devices(x)

    assert len(OutputDevice.registry) == 4

    register_config_rules(x)

    assert len(ControlRule.registry) == 4
