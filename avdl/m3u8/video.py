from pathlib import Path
import subprocess

import click


TIME_PROGRESS_PREFIX = 'out_time='


def combine_parts(output: Path,
                  *,
                  index: Path) -> None:
    assert index.is_file()

    # concat
    click.echo('Combining output file using ffmpeg ...')
    proc = subprocess.Popen([
        'ffmpeg',
        '-loglevel', 'fatal',
        '-progress', 'pipe:1',
        '-f', 'concat',
        '-i', str(index),
        '-c', 'copy',
        str(output)
    ], stdout=subprocess.PIPE)
    if proc.stdout is not None:
        for line_b in proc.stdout:
            line = line_b.decode().strip()
            if line.startswith(TIME_PROGRESS_PREFIX):
                click.echo(line + '  \r', nl=False)
    proc.wait()
