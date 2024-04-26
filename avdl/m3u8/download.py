import asyncio
import shutil
from pathlib import Path
from typing import Sequence

import click
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientPayloadError
from yarl import URL

from avdl.m3u8.constant import INDEX_NAME
from avdl.utils.console import print_error


async def download_m3u8_parts(url_base: URL,
                              parts: Sequence[URL],
                              *,
                              headers: dict[str, str],
                              cache_dir: Path,
                              retries: int) -> None:
    async with ClientSession(headers=headers) as session:
        # prepare dir
        cache_dir.mkdir(parents=True)

        # write index
        index_file = cache_dir / INDEX_NAME
        with open(index_file, 'w') as f:
            for part in parts:
                f.write(f'file {part.name}\n')

        # download parts
        with click.progressbar(length=len(parts),
                               label='Downloading',
                               width=shutil.get_terminal_size()[0]//2) as bar:
            lock = asyncio.Lock()

            async def download(part: URL) -> None:
                url = part if part.is_absolute() else url_base / part.name
                async with session.get(url) as response:
                    data = await response.read()
                    with open(cache_dir / part.name, 'wb') as f:
                        f.write(data)
                        async with lock:
                            bar.update(1)

            async def download_with_retry(part: URL) -> None:
                # retry-loop
                for _ in range(retries):
                    try:
                        await download(part)
                        break
                    except (TimeoutError, ClientPayloadError):
                        continue
                    except Exception as e:
                        print_error(str(e))
                        continue
                else:
                    # max retry reached
                    raise TimeoutError(f'{retries=}, {part=}')

            await asyncio.gather(*[download_with_retry(part) for part in parts])


def clean_up_cache(cache_dir: Path) -> None:
    # remove self cache
    if cache_dir.is_dir():
        shutil.rmtree(cache_dir)

    # remove parent cache dir if empty
    try:
        cache_dir.parent.rmdir()
    except OSError:
        pass
