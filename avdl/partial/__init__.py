import click


@click.command
def partial(
) -> None:
    print('This will do 206 partial content request')
