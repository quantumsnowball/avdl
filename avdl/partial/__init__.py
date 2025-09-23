from pathlib import Path

import click

from avdl.m3u8.constant import DEFAULT_HEADERS
from avdl.partial.curl import Curl
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
    headers = dict(**DEFAULT_HEADERS, **kv_split(header), )

    # output file
    output_file = Path(output)

    # appending data loop
    start_byte = 0
    total_bytes = 0
    while True:
        with Curl(url, headers, start=start_byte) as data:
            print(f'{data.start_byte=}, {data.end_byte=}, {data.total_bytes=}')
            data.append_to(output_file)
            total_bytes = data.total_bytes
            start_byte = data.end_byte + 1
        if start_byte >= total_bytes:
            break
