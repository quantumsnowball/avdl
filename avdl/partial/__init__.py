from io import BytesIO
from pathlib import Path

import click
import pycurl

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
    resp_headers = BytesIO()
    resp_body = BytesIO()
    c = pycurl.Curl()
    c.setopt(pycurl.HTTP_VERSION, pycurl.CURL_HTTP_VERSION_2_0)
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.HTTPHEADER, [f'{k}: {v}' for k, v in headers.items()])
    c.setopt(pycurl.WRITEDATA, resp_body)
    c.setopt(pycurl.HEADERFUNCTION, resp_headers.write)
    try:
        c.perform()
        status_code = c.getinfo(pycurl.RESPONSE_CODE)
        print(f'{status_code=}')
    except pycurl.error as e:
        print(f'{e=}')
    finally:
        c.close()
        resp_headers.close()
        resp_body.close()
