import subprocess
from pathlib import Path

import click

from raspcuterie import base_path
from raspcuterie.cli import cli


@cli.group()
def install():
    pass


@install.command()
def systemd():

    input_path = base_path / "raspcuterie.service"

    commands = [
        f"sudo cp {input_path} /etc/systemd/system",
        "sudo systemctl daemon-reload",
        "sudo systemctl enable raspcuterie.service",
        "sudo systemctl start raspcuterie",
    ]

    for command in commands:
        click.echo(command)
        print(subprocess.call(command.split(" ")))


@install.command()
def cron():

    command = "* * * * * /usr/local/bin/raspcuterie log-values"

    cron_in = subprocess.Popen(["crontab", "-l"], stdout=subprocess.PIPE)
    cur_crontab, _ = cron_in.communicate()

    cur_crontab = cur_crontab.decode("utf-8")

    if command not in cur_crontab:
        click.echo("Updating cronjob")
        cur_crontab += "# raspcuterie every minute"
        cur_crontab += command
    else:
        click.echo("Command already present")

    cron_out = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE)
    cron_out.communicate(input=cur_crontab.encode("utf-8"))


@cli.command()
def config():

    file = base_path / "config.yaml"

    if not base_path.exists():
        base_path.mkdir()

    if not file.exists():
        x = Path("./config.yaml")
        file.write_bytes(x.read_bytes())

    click.edit(filename=file)
