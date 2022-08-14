import importlib
import os
import pkgutil
import typing as t


class ProviderInfo:
    '''A data class that holds info of the CI provider such as Github Actions, Gitlab, or CircleCI.'''

    shared: t.Optional['ProviderInfo'] = None

    def __init__(self, name: str, module: str) -> None:
        self.name = name
        self.module = module

    @staticmethod
    def resolve_name() -> str:
        '''Resolve the name of the CI provider.'''

        if os.getenv('GITLAB_CI') == 'true':
            return 'gitlab'
        if os.getenv('GITHUB_ACTIONS') == 'true':
            return 'github'
        return 'github'

    @staticmethod
    def resolve() -> 'ProviderInfo':
        '''Resolve the CI provider info.

        Classes of the provider must be placed under ``cicd.providers.<name>``.
        They will be automatically loaded when resolving the provider info.
        '''

        name = ProviderInfo.resolve_name()
        module = f'cicd.providers.{name}'
        provider = importlib.import_module(module)
        for _, submodule, _ in pkgutil.iter_modules(provider.__path__):
            importlib.import_module(f'{module}.{submodule}')
        ProviderInfo.shared = ProviderInfo(name=name, module=module)
        return ProviderInfo.shared
