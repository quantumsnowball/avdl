import re
from functools import cached_property
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
        print(f'{self.start_byte=}, {self.end_byte=}, {self.total_bytes=}')

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

    @property
    def response_headers(self) -> list[str]:
        return self._resp_headers.getvalue().decode().splitlines()

    @cached_property
    def _content_range_info(self) -> tuple[int, ...]:
        content_range_line = next(line for line in self.response_headers if line.startswith('content-range'))
        match = re.match(r'content-range: bytes (\d+)-(\d+)/(\d+)', content_range_line)
        assert match, 'Error finding content-range data'
        return tuple(map(int, match.groups()))

    @property
    def start_byte(self) -> int:
        return self._content_range_info[0]

    @property
    def end_byte(self) -> int:
        return self._content_range_info[1]

    @property
    def total_bytes(self) -> int:
        return self._content_range_info[2]
