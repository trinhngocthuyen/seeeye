import importlib
import os
import pkgutil
from typing import Optional


class ProviderInfo:
    shared: Optional['ProviderInfo'] = None

    def __init__(self, name: str, module: str) -> None:
        self.name = name
        self.module = module

    @staticmethod
    def resolve_name() -> str:
        if os.getenv('GITLAB_CI') == 'true':
            return 'gitlab'
        if os.getenv('GITHUB_ACTIONS') == 'true':
            return 'github'
        return 'github'

    @staticmethod
    def resolve() -> 'ProviderInfo':
        name = ProviderInfo.resolve_name()
        module = f'cicd.providers.{name}'
        provider = importlib.import_module(module)
        for _, submodule, _ in pkgutil.iter_modules(provider.__path__):
            importlib.import_module(f'{module}.{submodule}')
        ProviderInfo.shared = ProviderInfo(name=name, module=module)
        return ProviderInfo.shared
