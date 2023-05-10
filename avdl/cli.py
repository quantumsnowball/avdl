from aiohttp import ClientSession
import click
import asyncio

from yarl import URL
from avdl.m3u8.constant import DEFAULT_HEADERS
from avdl.m3u8.download import download_m3u8_parts
from avdl.m3u8.playlist import async_fetch_m3u8
from avdl.utils.text import kv_split


@click.group()
def avdl() -> None:
    pass


@avdl.command()
@click.argument('url', type=str, default=None, required=False)
@click.option('-H', '--header', multiple=True, help='request header field')
@click.option('-o', '--output', default=None, required=False, help='save as filename')
@click.option('--limit', type=int, default=None, required=False, help='part limit')
def m3u8(url: str,
         header: list[str],
         output: str,
         limit: int | None) -> None:
    # parse inputs
    if url is None:
        url = click.prompt('Please input a m3u8 video url:', prompt_suffix='\n>>> ', type=str)
    assert len(url) > 0
    req_url = URL(url)
    req_headers = dict(**DEFAULT_HEADERS, **kv_split(header), )

    async def download() -> None:
        # shared session
        async with ClientSession(headers=req_headers) as session:
            # fetch playlist
            parts = await async_fetch_m3u8(req_url, session=session)
            if limit is not None:
                parts = parts[:limit]
            click.echo(f'Total parts: {len(parts)}')
            # start download async
            await download_m3u8_parts(req_url.parent, parts)
    asyncio.run(download())
    # ffmpeg concat
    # save as output
    click.echo(f'gonna save as {output}')
