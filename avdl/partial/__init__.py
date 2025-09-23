import re
from io import BytesIO
from pathlib import Path

import click
import pycurl

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

    # # curl requests
    # resp_headers = BytesIO()
    # resp_body = BytesIO()
    # c = pycurl.Curl()
    # c.setopt(pycurl.HTTP_VERSION, pycurl.CURL_HTTP_VERSION_2_0)
    # c.setopt(pycurl.URL, url)
    # c.setopt(pycurl.HTTPHEADER, [f'{k}: {v}' for k, v in headers.items()])
    # c.setopt(pycurl.HEADERFUNCTION, resp_headers.write)
    # c.setopt(pycurl.WRITEDATA, resp_body)
    # try:
    #     # send
    #     c.perform()
    #
    #     # should response 206
    #     status_code = c.getinfo(pycurl.RESPONSE_CODE)
    #     assert status_code == 206, 'Error receiving partial content'
    #
    #     # get header infos
    #     resp_headers_lines = resp_headers.getvalue().decode().splitlines()
    #     content_range_line = next(line for line in resp_headers_lines if line.startswith('content-range'))
    #     match = re.match(r'content-range: bytes (\d+)-(\d+)/(\d+)', content_range_line)
    #     assert match, 'Error finding content-range data'
    #     start_byte, end_byte, total_bytes = map(int, match.groups())
    #     print(f'{start_byte=}, {end_byte=}, {total_bytes=}')
    #
    #     # save the bytes to output_file
    #     with open(output_file, 'wb') as f:
    #         f.write(resp_body.getvalue())
    #
    # except pycurl.error as e:
    #     print(e)
    # finally:
    #     c.close()
    #     resp_headers.close()
    #     resp_body.close()

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
