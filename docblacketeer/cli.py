import click
from docblacketeer.code_formatter import sanitize_doctest_code
import io


@click.command()
@click.help_option()
def docblacketeer():
    """
    Wrapper around black to format passed python prompt text. Reads only from
    stdin.

    E.g. prompt text

    >>> x = 2 + 2
    >>> x
    4

    """
    read_stdin: io.TextIOWrapper = click.get_text_stream("stdin")
    sanitized: str = sanitize_doctest_code(read_stdin.read())
    click.echo(sanitized, nl=False)
