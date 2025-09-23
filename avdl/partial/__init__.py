from pathlib import Path

import click
from yarl import URL


@click.command
@click.argument('url', type=str, required=True)
@click.option('-o', '--output', required=True, help='save as filename')
def partial(
    url: str,
    output: str,
) -> None:
    req_url = URL(url)
    output_file = Path(output)
    print(f'Will download {req_url} and save as {output_file}')
