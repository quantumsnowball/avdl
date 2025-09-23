import re
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

    # curl requests
    resp_headers = BytesIO()
    resp_body = BytesIO()
    c = pycurl.Curl()
    c.setopt(pycurl.HTTP_VERSION, pycurl.CURL_HTTP_VERSION_2_0)
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.HTTPHEADER, [f'{k}: {v}' for k, v in headers.items()])
    c.setopt(pycurl.HEADERFUNCTION, resp_headers.write)
    c.setopt(pycurl.WRITEDATA, resp_body)
    try:
        # send
        c.perform()

        # get header infos
        resp_headers_lines = resp_headers.getvalue().decode().splitlines()
        content_range_line = next(line for line in resp_headers_lines if line.startswith('content-range'))
        match = re.match(r'content-range: bytes (\d+)-(\d+)/(\d+)', content_range_line)
        assert match, 'Error finding content-range data'
        start_byte, end_byte, total_bytes = map(int, match.groups())
        print(f'{start_byte=}, {end_byte=}, {total_bytes=}')

        # on response 206, save the bytes to output_file
        status_code = c.getinfo(pycurl.RESPONSE_CODE)
        assert status_code == 206, 'Error receiving partial content'
        with open(output_file, 'wb') as f:
            f.write(resp_body.getvalue())

    except pycurl.error as e:
        print(e)
    finally:
        c.close()
        resp_headers.close()
        resp_body.close()
