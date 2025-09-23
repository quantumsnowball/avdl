import re
from io import BytesIO
from pathlib import Path
from typing import Self

import pycurl


class Curl:
    def __init__(
        self,
        url: str,
        headers: dict[str, str],
    ) -> None:
        self._url = url
        self._req_headers = headers
        self._curl = pycurl.Curl()
        self._resp_headers = BytesIO()
        self._resp_body = BytesIO()
        curl = pycurl.Curl()
        curl.setopt(pycurl.HTTP_VERSION, pycurl.CURL_HTTP_VERSION_2_0)
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.HTTPHEADER, [f'{k}: {v}' for k, v in headers.items()])
        curl.setopt(pycurl.HEADERFUNCTION, self._resp_headers.write)
        curl.setopt(pycurl.WRITEDATA, self._resp_body)
        self._curl = curl

    def __enter__(self) -> Self:
        # send
        self._curl.perform()

        # should response 206
        assert self.status_code == 206, 'Error receiving partial content'

        # get header infos
        resp_headers_lines = self._resp_headers.getvalue().decode().splitlines()
        content_range_line = next(line for line in resp_headers_lines if line.startswith('content-range'))
        match = re.match(r'content-range: bytes (\d+)-(\d+)/(\d+)', content_range_line)
        assert match, 'Error finding content-range data'
        start_byte, end_byte, total_bytes = map(int, match.groups())
        print(f'{start_byte=}, {end_byte=}, {total_bytes=}')

        #
        return self

    def __exit__(self, *_):
        # Clean up resources
        self._curl.close()
        self._resp_headers.close()
        self._resp_body.close()

    @property
    def status_code(self) -> int:
        return self._curl.getinfo(pycurl.RESPONSE_CODE)
