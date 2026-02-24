from pathlib import Path
from typing import Annotated

import typer
from alive_progress import alive_bar
from typer import Argument, Option

from avdl.m3u8.constant import DEFAULT_HEADERS
from avdl.partial.curl import Curl
from avdl.utils.text import kv_split

app = typer.Typer()


@app.command()
def partial(
    url: Annotated[str, Argument(help='URL of the partial file')],
    output: Annotated[str, Option('--output', '-o', help='save as filename')],
    header: Annotated[list[str], Option('--header', '-H', help='request header field')] = [],
) -> None:
    # request header
    headers = dict(**DEFAULT_HEADERS, **kv_split(header), )

    # output file
    output_file = Path(output)
    if output_file.exists():
        if input(f'{output_file.name} already exists, overwrite? y/[n]: ').lower() != 'y':
            return
        output_file.unlink()

    # appending data loop
    start_byte = 0
    total_bytes = 0
    with alive_bar(manual=True) as bar:
        while True:
            with Curl(url, headers, start=start_byte) as data:
                total_bytes = data.total_bytes
                data.append_to(output_file)
                bar.text(f'Downloading: {(data.end_byte + 1)/1e6:,.2f} / {total_bytes/1e6:,.2f} MB')
                bar(data.progress)
                start_byte = data.end_byte + 1
            if start_byte >= total_bytes:
                bar(1.0)
                break
