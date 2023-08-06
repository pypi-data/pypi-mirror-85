import shlex
from unittest import mock

from click.testing import CliRunner

from .cli import create_cli


def test_init():
    manager = mock.MagicMock()

    runner = CliRunner()
    cli = create_cli(manager)
    result = runner.invoke(cli, shlex.split('init'))

    assert result.exit_code == 0
    manager.create_config.assert_called()


def test_check():
    manager = mock.MagicMock()

    runner = CliRunner()
    cli = create_cli(manager)
    result = runner.invoke(cli, shlex.split('check'))

    assert result.exit_code == 0
    manager.check_config.assert_called()


def test_serve():
    manager = mock.MagicMock()

    runner = CliRunner()
    cli = create_cli(manager)
    result = runner.invoke(cli, shlex.split('serve'))

    assert result.exit_code == 0
    manager.serve.assert_called_with(
        host='0.0.0.0',
        port=9527,
    )
