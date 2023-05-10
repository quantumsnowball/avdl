import click
import asyncio
from avdl.m3u8.constant import DEFAULT_HEADERS
from avdl.m3u8.playlist import async_fetch_m3u8


@click.group()
def avdl() -> None:
    pass


@avdl.command()
def m3u8() -> None:
    url = input('Please input a m3u8 video url:\n>>> ')
    print('Custom header? (Type name:value/Enter to finish)')
    headers = {
        **DEFAULT_HEADERS,
    }
    while True:
        line = input()
        if not line:
            break
        key, val = map(str.strip, line.split(':', 1))
        headers[key] = val
    task = async_fetch_m3u8(url, headers)
    asyncio.run(task)
