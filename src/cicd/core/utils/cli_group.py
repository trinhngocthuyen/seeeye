import functools
import pkgutil

import click

__all__ = ['cli_group']


def create_cli_group(module_name: str, target: click.Command):
    import importlib

    module = importlib.import_module(module_name)
    for _, submodule_name, _ in pkgutil.iter_modules(module.__path__):
        submodule = importlib.import_module(f'{module_name}.{submodule_name}')
        if submodule_name != 'cli' and hasattr(submodule, 'cli'):
            command = getattr(submodule, 'cli')
            target.add_command(command, name=submodule_name)


def cli_group(name: str):
    def decorator(func: click.Command):
        @functools.wraps(func)
        @click.group()
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        create_cli_group(name, target=wrapper)
        return wrapper

    return decorator
