import asyncio
import shutil
from pathlib import Path
from typing import Sequence

import click
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientPayloadError
from yarl import URL

from avdl.m3u8.constant import INDEX_NAME, PART_DIRNAME
from avdl.utils.logging import LOG_FILENAME, create_logger


async def download_m3u8_parts(url_base: URL,
                              parts: Sequence[URL],
                              *,
                              headers: dict[str, str],
                              cache_dir: Path,
                              retries: int,
                              debug: bool) -> None:
    async with ClientSession(headers=headers) as session:
        # prepare dir
        part_dir = cache_dir / PART_DIRNAME
        part_dir.mkdir(parents=True)

        # logger
        logger = create_logger(__name__,
                               'DEBUG' if debug else 'WARNING',
                               cache_dir / LOG_FILENAME)

        # write index
        index_file = part_dir / INDEX_NAME
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
                    with open(part_dir / part.name, 'wb') as f:
                        f.write(data)
                        async with lock:
                            bar.update(1)

            async def download_with_retry(part: URL) -> None:
                # retry-loop
                for _ in range(retries):
                    try:
                        await download(part)
                        logger.debug(f'Downloaded {part}')
                        break
                    except (TimeoutError, ClientPayloadError) as e:
                        logger.error(e, exc_info=True)
                        continue
                    except Exception as e:
                        logger.critical(e, exc_info=True)
                        continue
                else:
                    # max retry reached
                    raise TimeoutError(f'{retries=}, {part=}')

            await asyncio.gather(*[download_with_retry(part) for part in parts])


def clean_up_cache(cache_dir: Path) -> None:
    # remove parts cache
    part_dir = cache_dir / PART_DIRNAME
    if part_dir.is_dir():
        shutil.rmtree(part_dir)

    # remove parent cache dirs if empty
    try:
        cache_dir.rmdir()
        cache_dir.parent.rmdir()
    except OSError:
        pass
