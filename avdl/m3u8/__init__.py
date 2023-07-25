from pathlib import Path
import click
import asyncio

from yarl import URL
from avdl.m3u8.constant import CACHE_DIR_PARENT, DEFAULT_HEADERS, INDEX_NAME
from avdl.m3u8.download import clean_up_cache, download_m3u8_parts
from avdl.m3u8.playlist import async_fetch_m3u8
from avdl.m3u8.video import combine_parts
from avdl.utils.console import print_exception, print_key_value, print_success, print_warning, require_user_input
from avdl.utils.text import kv_split


@click.command()
@click.argument('url', type=str, default='', required=False)
@click.option('-H', '--header', multiple=True, help='request header field')
@click.option('-o', '--output', default=None, required=False, help='save as filename')
@click.option('--limit', type=int, default=None, required=False, help='part limit')
@click.option('--retries', type=int, default=20, required=False, help='attempts to retry when timeout')
def m3u8(url: str,
         header: list[str],
         output: str,
         limit: int | None,
         retries: int) -> None:
    # request header
    req_headers = dict(**DEFAULT_HEADERS, **kv_split(header), )

    # loop until fetched a valid playlist
    while True:
        # ask for url if user not provided, or if fetch playlist failed
        if not url:
            url = require_user_input('Please input a m3u8 video url')
        req_url = URL(url)

        try:
            # fetch playlist
            parts, info = asyncio.run(async_fetch_m3u8(req_url, headers=req_headers))
            print_key_value('duration', f'{info["duration"]} ({info["count"]} parts)')
            break
        except Exception as e:
            # reset url input
            url = ''
            print_exception(e)
            continue

    # trim if limit
    if limit is not None:
        parts = parts[:limit]
        print_warning(f'Only downloading the first {len(parts)} parts')

    # ask for save filename if not already exists
    if output is None:
        output = require_user_input('Please input output filename')

    # define paths
    output_file = Path(output)
    cache_dir = CACHE_DIR_PARENT / output_file
    index_file = cache_dir / INDEX_NAME

    # download
    asyncio.run(download_m3u8_parts(req_url.parent, parts,
                                    headers=req_headers,
                                    cache_dir=cache_dir,
                                    retries=retries))

    # ffmpeg concat
    combine_parts(output_file,
                  index=index_file,
                  total_seconds=info['total_seconds'])

    # confirmation
    assert output_file.is_file()
    print_success(f'Saved as {output_file}')

    # cleanup
    clean_up_cache(cache_dir)
