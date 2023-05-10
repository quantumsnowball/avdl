from collections.abc import Iterable
from aiohttp import ClientSession
from yarl import URL


async def download_m3u8_parts(url_base: URL,
                              parts: Iterable[str],
                              *,
                              session: ClientSession) -> None:
    async def download(url: URL) -> None:
        pass

    for part in parts:
        print(url_base / part)
