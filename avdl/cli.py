import click

from avdl.m3u8 import m3u8
from avdl.partial import partial


@click.group()
def avdl() -> None:
    pass


avdl.add_command(m3u8)
avdl.add_command(partial)
