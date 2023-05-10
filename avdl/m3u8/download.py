from pathlib import Path
import asyncio
from collections.abc import Iterable
from aiohttp import ClientSession
import click
from yarl import URL


CACHE_DIR_PARENT = '.avdl'


async def download_m3u8_parts(url_base: URL,
                              parts: Iterable[str],
                              *,
                              output: Path,
                              session: ClientSession) -> None:
    cache_dir = CACHE_DIR_PARENT / output
    cache_dir.mkdir(parents=True)

    async def download(part: str) -> None:
        async with session.get(url_base / part) as response:
            data = await response.read()
            with open(cache_dir / part, 'wb') as f:
                f.write(data)
                click.echo(f'{part}')

    tasks = [download(part)
             for part in parts]
    await asyncio.gather(*tasks)
