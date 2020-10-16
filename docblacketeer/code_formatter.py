from black import format_str, Mode
import re
from typing import List, Tuple

ARROWS = ">>> "
DOTS = "... "


class CodeParseError(Exception):
    """
    Raised when code cannot be parsed.
    """


def black_str_formatter(str_to_format: str) -> str:
    """
    The passed string is valid python that is returned with black formatting
    applied.
    """
    return format_str(str_to_format, mode=Mode())


def clean_doctest_code_of_symbols(doctest_code: str) -> str:
    """
    Cleans python code that contains typical prompt symbols e.g. '>>>'
    """
    symbols_stripped = doctest_code.replace(">>> ", "").replace(">>>", "")
    return symbols_stripped


def define_prefix(line_of_code: str) -> str:
    """
    Checks whether the prefix is dots or symbols or neither.

    Raises CodeParseError if both are found in a line of code.
    """
    arrows_regex = re.compile(f"^{ARROWS}")
    dots_regex = re.compile(f"^{DOTS}")
    arrows_matched = re.match(arrows_regex, line_of_code)
    dots_matched = re.match(dots_regex, line_of_code)
    if arrows_matched is None and dots_matched is None:
        return ""
    elif arrows_matched is not None:
        return ARROWS
    elif dots_matched is not None:
        return DOTS
    else:
        raise CodeParseError


def separate_last_lines(
    split_to_lines: List[str],
) -> Tuple[List[str], List[str], List[str]]:

    """
    Separates a list if strings to two lists with the pivot on the first line
    with no >>> or ...
    """
    pivot_idx = -1
    defined_prefixes = []
    for idx, line in enumerate(split_to_lines):
        defined_prefixes.append(define_prefix(line))
        if define_prefix(line) == "":
            pivot_idx = idx if pivot_idx == -1 else pivot_idx
    if pivot_idx == -1:
        raise CodeParseError("No prompt returns found.")
    last_lines = split_to_lines[pivot_idx:]
    other_lines = split_to_lines[:pivot_idx]

    for defined_prefix in defined_prefixes[pivot_idx:]:
        if defined_prefix != "":
            raise CodeParseError("Mixed returns and ARROWS and DOTS.")

    for defined_prefix in defined_prefixes[:pivot_idx]:
        if defined_prefix == "":
            raise CodeParseError(
                ">>> and ... symbols were not recognized succesfully."
                "\nThere might be whitespace before the arrows or dots."
            )

    return other_lines, last_lines, defined_prefixes


def check_and_fix_whitespaced_lines(
    black_formatted: List[str], defined_prefixes: List[str]
) -> Tuple[List[str], List[str]]:
    """
    Black might add whitespaced lines. These must be prefixed with >>> prefixes.
    """
    lines_with_whitespace = []
    for idx, line in enumerate(black_formatted):
        if line == "\n":
            lines_with_whitespace.append(idx)
    if len(lines_with_whitespace) == 0:
        return black_formatted, defined_prefixes
    else:
        for idx in lines_with_whitespace:
            defined_prefixes.insert(idx, ARROWS)
    if len(black_formatted) == len(defined_prefixes):
        raise CodeParseError(
            "black_formatted and defined_prefixes have different lengths."
            f"{len(black_formatted), len(defined_prefixes)}"
        )
    return black_formatted, defined_prefixes


def sanitize_doctest_code(code_to_sanitize: str) -> str:
    """
    Sanitizes passed doctesting code with black and returns it.
    """
    if len(code_to_sanitize) == 0:
        return ""
    if not isinstance(code_to_sanitize, str):
        raise CodeParseError(
            f"Did not receive string data in sanitize_doctest_code."
            f"code_to_sanitize: {code_to_sanitize}, Type: {type(code_to_sanitize)}]"
        )
    if ARROWS not in code_to_sanitize:
        raise CodeParseError(
            "code_to_sanitize does not contain >>>. "
            "Cannot interpret as doctest code."
        )
    # Split passed string data into lines.
    split_to_lines = code_to_sanitize.splitlines(keepends=True)
    # Separate prompt return lines (no >>> or ...) from prompt input lines
    # with arrows or dots.
    other_lines, last_lines, defined_prefixes = separate_last_lines(split_to_lines)
    assert len(other_lines + last_lines) == len(defined_prefixes)
    # Separate last lines (return lines in prompt). No formatting is required for them.
    other_lines_joined = "".join(other_lines)
    # Clean code of prompt symbols >>> and ...
    cleaned_of_doctest_symbols = clean_doctest_code_of_symbols(other_lines_joined)
    # Format code through black
    black_formatted = black_str_formatter(cleaned_of_doctest_symbols).splitlines(
        keepends=True
    )
    # Check if black added whitespaced lines
    if len(black_formatted) != len(other_lines):
        black_formatted, defined_prefixes = check_and_fix_whitespaced_lines(
            black_formatted, defined_prefixes
        )
    joined_with_prefix = [
        prefix + line
        for prefix, line in
        # lambda prefix, line: f"{prefix} {line}",
        zip(defined_prefixes, black_formatted + last_lines)
    ]
    return "".join(joined_with_prefix)
