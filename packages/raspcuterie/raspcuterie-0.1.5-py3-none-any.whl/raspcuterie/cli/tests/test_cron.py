from .. import cron


def test_log_values(runner):
    result = runner.invoke(cron.log_values, catch_exceptions=False)
    assert result.exit_code == 0, result.exception
