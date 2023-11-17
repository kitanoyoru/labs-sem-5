import click

from .commands.reset_db_command import reset_db
from .commands.send_request_command import send_request


@click.group()
def cli():
    pass


cli.add_command(send_request)
cli.add_command(reset_db)
