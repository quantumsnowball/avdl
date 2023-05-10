import asyncio
from collections.abc import Iterable
from aiohttp import ClientSession
from yarl import URL


async def download_m3u8_parts(url_base: URL,
                              parts: Iterable[str],
                              *,
                              session: ClientSession) -> None:
    async def download(url: URL) -> None:
        print(f'downloading {url}')

    tasks = [download(url_base / part)
             for part in parts]
    await asyncio.gather(*tasks)
