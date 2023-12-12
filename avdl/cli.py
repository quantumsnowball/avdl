import click

from avdl.m3u8 import m3u8


@click.group()
def avdl() -> None:
    pass


avdl.add_command(m3u8)
