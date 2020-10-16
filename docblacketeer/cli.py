import click
from docblacketeer.code_formatter import sanitize_doctest_code


@click.command()
def docblacketeer():
    read_stdin = click.get_text_stream("stdin")
    sanitized = sanitize_doctest_code(read_stdin)
    click.echo(sanitized, nl=False)
