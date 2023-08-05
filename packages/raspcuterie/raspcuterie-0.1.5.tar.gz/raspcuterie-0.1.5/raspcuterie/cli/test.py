import click

from raspcuterie.cli import cli, with_appcontext
from raspcuterie.devices import InputDevice, OutputDevice


@cli.group()
def test():
    pass


@test.command()
@with_appcontext
def devices():
    click.echo("Listing input devices:")
    click.echo("============================")

    for key, device in InputDevice.registry.items():
        try:
            click.echo(f"{key}: {device.read()}")
        except Exception as e:
            click.echo(click.style(f"{key}: {e}", fg="red"), err=True)

    click.echo("Listing output devices:")
    click.echo("============================")

    for key, device in OutputDevice.registry.items():
        try:
            click.echo(f"{key}: {device.value()}")
        except Exception as e:
            click.echo(click.style(f"{key}: {e}", fg="red"), err=True)
