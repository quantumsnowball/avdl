import typer

from avdl.m3u8 import app as m3u8

app = typer.Typer(
    no_args_is_help=True,
)


app.add_typer(m3u8)
# app.add_typer(partial, name='m3u8')

if __name__ == "__main__":
    app()
