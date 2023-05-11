from pathlib import Path
import subprocess

import click

from avdl.utils.console import print_warning
from datetime import datetime


TIME_PROGRESS_PREFIX = 'out_time='


def combine_parts(output: Path,
                  *,
                  index: Path,
                  total_seconds: int) -> None:
    assert index.is_file()

    # concat
    print_warning('Combining output file using ffmpeg ...')
    proc = subprocess.Popen([
        'ffmpeg',
        '-loglevel', 'fatal',
        '-progress', 'pipe:1',
        '-f', 'concat',
        '-i', str(index),
        '-c', 'copy',
        str(output)
    ], stdout=subprocess.PIPE)

    # progress
    if proc.stdout is not None:
        with click.progressbar(length=total_seconds,
                               label='Combining',
                               width=click.get_terminal_size()[0]//2) as bar:
            for line_b in proc.stdout:
                line = line_b.decode().strip()
                try:
                    if line.startswith(TIME_PROGRESS_PREFIX):
                        current_time = line.split('=', maxsplit=1)[1]
                        current_second = round((datetime.strptime(current_time, '%H:%M:%S.%f') -
                                                datetime.strptime('00:00:00.000000', '%H:%M:%S.%f')).total_seconds())
                        bar.update(current_second)
                except ValueError:
                    pass
            # ensure 100%
            bar.update(total_seconds)

    # join
    proc.wait()
