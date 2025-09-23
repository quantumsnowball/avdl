from pathlib import Path

import click
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
    req_headers = dict(**DEFAULT_HEADERS, **kv_split(header), )

    # request url
    req_url = URL(url)

    # output file
    output_file = Path(output)

    #
    print(f'Will download {req_url} and save as {output_file}')
    print(f'{req_headers=}')
