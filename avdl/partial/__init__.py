import click
from yarl import URL


@click.command
@click.argument('url', type=str, required=True)
def partial(
    url: str,
) -> None:
    req_url = URL(url)
    print(f'Will download {req_url}')
