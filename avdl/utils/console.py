from typing import Any

import click


def require_user_input(message: str,
                       *args: Any,
                       **kwargs: Any):
    styled_message = click.style(message, fg='cyan')
    return click.prompt(styled_message, *args, type=str, **kwargs)


def print_warning(message: str,
                  *args: Any,
                  **kwargs: Any):
    return click.secho(message, *args, fg='yellow', **kwargs)


def print_success(message: str,
                  *args: Any,
                  **kwargs: Any):
    return click.secho(message, *args, fg='green', **kwargs)


def print_key_value(message: str,
                    value: Any,
                    *args: Any,
                    **kwargs: Any):
    styled_message = click.style(message, fg='blue')
    return click.echo(f'{styled_message}: {str(value)}', *args, **kwargs)
