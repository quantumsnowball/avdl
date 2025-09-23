import asyncio
from pathlib import Path

import click
import httpx
import requests
from aiohttp import ClientSession
from yarl import URL

from avdl.m3u8.constant import DEFAULT_HEADERS
from avdl.utils.text import kv_split


@click.command
@click.argument('url', type=str, required=True)
@click.option('-H', '--header', multiple=True, help='request header field')
@click.option('-o', '--output', required=True, help='save as filename')
def partial(
    url: str,
    header: list[str],
    output: str,
) -> None:
    # request header
    headers = dict(**kv_split(header), )

    # output file
    output_file = Path(output)

    #
    with httpx.Client(http2=True) as client:
        resp = client.get(url, headers=headers)
        print(f'{resp.status_code=}')
    # from pprint import pprint as pp
    # resp = requests.get(url, headers=headers)
    # print(f'Will download {url} and save as {output_file}')
    # pp(req_headers)
    # print(f'{resp.status_code=}')
    # pp(dict(**resp.headers))
    # print(resp.content)
