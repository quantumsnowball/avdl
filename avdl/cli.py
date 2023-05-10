import click
import asyncio

from avdl.m3u8.playlist import async_fetch_m3u8


DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'


@click.group()
def avdl() -> None:
    pass


@avdl.command()
def m3u8() -> None:
    url = input('Please input a m3u8 video url:\n>>> ')
    print('Custom header? (Type name:value/Enter to finish)')
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US, en;q = 0.9',
        'User-Agent': DEFAULT_USER_AGENT,
    }
    while True:
        line = input()
        if not line:
            break
        key, val = map(str.strip, line.split(':', 1))
        headers[key] = val
    task = async_fetch_m3u8(url, headers)
    asyncio.run(task)
