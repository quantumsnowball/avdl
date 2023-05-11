from pathlib import Path
import asyncio
from typing import Sequence
from aiohttp import ClientSession
import click
from yarl import URL
import shutil

from avdl.m3u8.constant import INDEX_NAME
from avdl.utils.console import print_key_value


async def download_m3u8_parts(url_base: URL,
                              parts: Sequence[str],
                              *,
                              headers: dict[str, str],
                              cache_dir: Path) -> None:
    async with ClientSession(headers=headers) as session:
        # prepare dir
        cache_dir.mkdir(parents=True)

        # write index
        index_file = cache_dir / INDEX_NAME
        with open(index_file, 'w') as f:
            for part in parts:
                f.write(f'file {part}\n')

        # download parts
        with click.progressbar(length=len(parts),
                               label='Download',
                               width=click.get_terminal_size()[0]//2) as bar:
            lock = asyncio.Lock()

            async def download(part: str) -> None:
                async with session.get(url_base / part) as response:
                    data = await response.read()
                    with open(cache_dir / part, 'wb') as f:
                        f.write(data)
                        async with lock:
                            bar.update(1)

            await asyncio.gather(*[download(part) for part in parts])

        # confirmation
        ts_file_count = sum(1 for _ in cache_dir.glob('*.ts'))
        print_key_value('\nTotal parts downloaded', ts_file_count)


def clean_up_cache(cache_dir: Path) -> None:
    # remove self cache
    if cache_dir.is_dir():
        shutil.rmtree(cache_dir)

    # remove parent cache dir if empty
    try:
        cache_dir.parent.rmdir()
    except OSError:
        pass
