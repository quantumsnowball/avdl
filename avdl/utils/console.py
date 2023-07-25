from typing import Any

import click


def require_user_input(message: str,
                       *args: Any,
                       non_empty: bool = True,
                       forbidden_chars: tuple[str, ...] = tuple(),
                       **kwargs: Any) -> str:
    styled_message = click.style(message, fg='cyan')
    while True:
        try:
            user_input = input(styled_message + ': ', *args, **kwargs)
            if non_empty and len(user_input) == 0:
                raise ValueError('Empty string is not allowed')
            for c in forbidden_chars:
                if c in user_input:
                    raise ValueError(f"Forbidden character: '{c}'")
            return user_input
        except Exception as e:
            print_exception(e)
            continue


def print_warning(message: str,
                  *args: Any,
                  **kwargs: Any) -> None:
    return click.secho(message, *args, fg='yellow', **kwargs)


def print_success(message: str,
                  *args: Any,
                  **kwargs: Any) -> None:
    return click.secho(message, *args, fg='green', **kwargs)


def print_error(message: str,
                *args: Any,
                **kwargs: Any) -> None:
    return click.secho(message, *args, fg='red', **kwargs)


def print_exception(e: Exception) -> None:
    print_error(f'{e.__class__.__name__}: {str(e)}')


def print_key_value(message: str,
                    value: Any,
                    *args: Any,
                    **kwargs: Any) -> None:
    styled_message = click.style(message, fg='blue')
    return click.echo(f'{styled_message}: {str(value)}', *args, **kwargs)
