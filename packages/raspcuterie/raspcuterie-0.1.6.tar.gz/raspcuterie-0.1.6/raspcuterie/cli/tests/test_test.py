from .. import test


def test_devices(runner):

    result = runner.invoke(test.devices, catch_exceptions=False)
    assert result.exit_code == 0, result.exception

