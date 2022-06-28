from typing import TypeVar

from cicd.core.provider import ProviderInfo

T = TypeVar('T', bound='ProviderMixin')


class ProviderMixin:
    def as_provider(self: T) -> T:
        provider_info = self.provider_info
        klazz = next(
            klazz
            for klazz in self.__class__.__subclasses__()
            if klazz.__module__.startswith(provider_info.module)
        )
        return klazz()

    @property
    def provider(self: T) -> T:
        try:
            return self._provider
        except:
            self._provider = self.as_provider()
            return self._provider

    @property
    def provider_info(self) -> ProviderInfo:
        return ProviderInfo.resolve()
