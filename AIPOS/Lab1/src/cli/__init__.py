import click

from .commands.send_request_command import send_request


@click.group()
def cli():
    pass


cli.add_command(send_request)
