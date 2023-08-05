import functools

import click

from raspcuterie.app import create_app


def with_appcontext(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        app = create_app()

        with app.app_context():
            return func(*args, **kwargs)

    return decorator


@click.group()
def cli():
    pass


from . import cron, fake, test, install  # noqa
