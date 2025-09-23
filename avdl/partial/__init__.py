from pathlib import Path

import click
import pycurl as curl

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
    c = curl.Curl()
    c.setopt(curl.HTTP_VERSION, curl.CURL_HTTP_VERSION_2_0)
    c.setopt(curl.URL, url)
    c.setopt(curl.HTTPHEADER, [f'{k}: {v}' for k, v in headers.items()])
    c.perform()
    status_code = c.getinfo(curl.RESPONSE_CODE)
    print(f'{status_code=}')
    c.close()
