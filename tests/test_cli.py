from click.testing import CliRunner
from docblacketeer.cli import docblacketeer
from docblacketeer.code_formatter import CodeParseError
from tests import TestParameters
import pytest


@pytest.mark.parametrize(
    "stdin_input,expected", TestParameters.list_of_prompt_code_with_expected
)
def test_command_line_integration(stdin_input, expected):
    """
    Tests click functionality.
    """
    clirunner = CliRunner()
    result = clirunner.invoke(docblacketeer, input=stdin_input)
    if expected is CodeParseError:
        assert result.exit_code == 1
    else:
        # Check that exit code is 0 (i.e. ran succesfully.)
        assert result.exit_code == 0
        # Checks if output path is printed
        assert str(">>>") in result.output


def test_command_line_integration_no_stdin():
    clirunner = CliRunner()
    result = clirunner.invoke(docblacketeer)
    # Check that exit code is 0 (i.e. ran succesfully.)
    assert result.exit_code == 0
    assert result.output is ""
