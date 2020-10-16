import pytest
from docblacketeer import code_formatter
from docblacketeer.code_formatter import ARROWS, DOTS
from tests import TestParameters


@pytest.mark.parametrize("str_to_format", TestParameters.list_of_valid_python_code)
def test_black_str_formatter(str_to_format: str):
    result = code_formatter.black_str_formatter(str_to_format)
    assert isinstance(result, str)


@pytest.mark.parametrize("doctest_code", TestParameters.list_of_prompt_code)
def test_clean_doctest_code_of_symbols(doctest_code: str):
    result = code_formatter.clean_doctest_code_of_symbols(doctest_code)
    assert isinstance(result, str)


@pytest.mark.parametrize(
    "code_to_sanitize,expected", TestParameters.list_of_prompt_code_with_expected
)
def test_sanitize_doctest_code(code_to_sanitize: str, expected):
    # If errors is expected -> catch it
    # and fail if no error
    if expected is code_formatter.CodeParseError:
        try:
            code_formatter.sanitize_doctest_code(code_to_sanitize)
        except code_formatter.CodeParseError:
            pass
        else:
            assert False
    else:
        result = code_formatter.sanitize_doctest_code(code_to_sanitize)
        assert isinstance(result, str)
        if expected is code_formatter.CodeParseError:
            try:
                code_formatter.sanitize_doctest_code(code_to_sanitize)
            except code_formatter.CodeParseError:
                pass
            else:
                assert False
        assert result == expected


@pytest.mark.parametrize("line_of_code,expected", TestParameters.lines_of_code)
def test_define_prefix(line_of_code, expected):
    result = code_formatter.define_prefix(line_of_code)
    assert result == expected
