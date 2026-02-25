# enable advance key press, e.g. arrow keys
import readline as readline

import typer

from .m3u8 import app as m3u8
from .partial import app as partial

app = typer.Typer(
    name='avdl',
    no_args_is_help=True,
    help='a video downloader',
)

app.add_typer(m3u8)
app.add_typer(partial)
