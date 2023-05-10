from pathlib import Path
import subprocess

import click


def combine_parts(output: Path,
                  *,
                  index: Path,
                  loglevel: str = 'info') -> None:
    assert index.is_file()

    # concat
    subprocess.run([
        'ffmpeg',
        '-loglevel', loglevel,
        '-f', 'concat',
        '-i', str(index),
        '-c', 'copy',
        str(output)
    ])

    # clean up cache dir
    pass
