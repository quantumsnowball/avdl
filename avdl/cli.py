import click
import asyncio
from avdl.m3u8.constant import DEFAULT_HEADERS
from avdl.m3u8.playlist import async_fetch_m3u8
from avdl.utils.text import kv_split


@click.group()
def avdl() -> None:
    pass


@avdl.command()
@click.argument('url', type=str, default=None, required=False)
@click.option('-H', '--header', multiple=True, help='request header field')
@click.option('-o', '--output', default=None, required=False, help='save as filename')
def m3u8(url: str,
         header: list[str],
         output: str) -> None:
    # parse inputs
    if url is None:
        url = click.prompt('Please input a m3u8 video url:', prompt_suffix='\n>>> ')
    req_headers = dict(**DEFAULT_HEADERS, **kv_split(header), )
    # fetch playlist
    playlist = asyncio.run(async_fetch_m3u8(url, req_headers))
    click.echo(f'Total parts: {len(playlist)}')
    # start download async
    # ffmpeg concat
    # save as output
    click.echo(f'gonna save as {output}')
