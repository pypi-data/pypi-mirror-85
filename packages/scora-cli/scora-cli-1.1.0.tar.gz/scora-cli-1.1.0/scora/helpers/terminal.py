import click
import sys


def title(txt):
    """Shows a bold title in the terminal

    Args:
        txt (str): The title to be shown
    """
    click.secho('')
    click.secho(txt, bold=True)
    click.secho('--------------------')


def prompt(*args, **kwargs):
    """Prompts the user a question.

    Args:
      prompt_method (func): The function that should be user to prompt, such \
        as click.confirm or click.prompt.

    Raises:
        Exception: Prompt function called without a method

    Returns:
        answer (any): The answer
    """

    prompt_method = kwargs.pop('prompt_method', None)
    if not prompt_method:
        raise Exception('Prompt function called without a method')

    try:
        return prompt_method(*args, **kwargs)
    except click.exceptions.Abort:
        click.secho('\nAborted!', fg='blue')
        sys.exit()
