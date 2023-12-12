import pytest
from click.testing import CliRunner

from avdl.cli import avdl


def test_cmd_avdl():
    runner = CliRunner()
    r1 = runner.invoke(avdl)
    assert r1.output.startswith('Usage:')


def test_cmd_avdl_m3u8():
    runner = CliRunner()
    r2 = runner.invoke(avdl, ['m3u8'])
    assert r2.exit_code == 1
