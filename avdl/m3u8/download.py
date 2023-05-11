from pathlib import Path
import asyncio
from collections.abc import Iterable
from aiohttp import ClientSession
import click
from yarl import URL
import shutil

from avdl.m3u8.constant import INDEX_NAME


async def download_m3u8_parts(url_base: URL,
                              parts: Iterable[str],
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
        async def download(part: str) -> None:
            async with session.get(url_base / part) as response:
                data = await response.read()
                with open(cache_dir / part, 'wb') as f:
                    f.write(data)
                    click.echo('.', nl=False)
        tasks = [download(part)
                 for part in parts]
        await asyncio.gather(*tasks)

        # confirmation
        ts_file_count = sum(1 for _ in cache_dir.glob('*.ts'))
        click.echo(f'\nTotal parts downloaded: {ts_file_count}')


def clean_up_cache(cache_dir: Path) -> None:
    # remove self cache
    if cache_dir.is_dir():
        shutil.rmtree(cache_dir)

    # remove parent cache dir if empty
    try:
        cache_dir.parent.rmdir()
    except OSError:
        pass
