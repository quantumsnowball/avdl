# enable advance key press, e.g. arrow keys
import readline as readline

import typer

from avdl.m3u8 import app as m3u8
from avdl.partial import app as partial

app = typer.Typer(no_args_is_help=True)

app.add_typer(m3u8)
app.add_typer(partial)
