from pathlib import Path
import asyncio
from collections.abc import Iterable
from aiohttp import ClientSession
import click
from yarl import URL

from avdl.m3u8.constant import INDEX_NAME


async def download_m3u8_parts(url_base: URL,
                              parts: Iterable[str],
                              *,
                              cache_dir: Path,
                              session: ClientSession) -> None:
    # prepare dir
    cache_dir.mkdir(parents=True)

    # write index
    index_file = cache_dir / INDEX_NAME
    with open(index_file, 'w') as f:
        for part in parts:
            f.write(f'file {part}\n')

    # download parts
    async def download(part: str) -> None:
        async with session.get(url_base / part) as response:
            data = await response.read()
            with open(cache_dir / part, 'wb') as f:
                f.write(data)
                click.echo('.', nl=False)
    tasks = [download(part)
             for part in parts]
    await asyncio.gather(*tasks)
