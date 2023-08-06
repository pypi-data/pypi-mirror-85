from typer.testing import CliRunner

from pier_mob import app
import pier_mob


runner = CliRunner()


def test_app():
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "--help" in result.stdout
    assert "info" in result.stdout
    assert "version" in result.stdout


def test_info():
    result = runner.invoke(app, ["info",])
    assert result.exit_code == 0
    assert "♥️" in result.stdout


def test_version():
    result = runner.invoke(app, ["version",])
    assert result.exit_code == 0
    assert pier_mob.cli.__version__ in result.stdout
