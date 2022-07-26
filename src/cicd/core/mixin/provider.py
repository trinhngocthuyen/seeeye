from functools import cached_property
from typing import Optional, TypeVar

from cicd.core.provider.info import ProviderInfo

T = TypeVar('T', bound='ProviderMixin')


class ProviderMixin:
    __provider_info__: Optional[ProviderInfo] = None

    def as_provider(self: T) -> T:
        return self.provider_cls()()

    @cached_property
    def provider(self: T) -> T:
        return self.as_provider()

    @property
    def provider_info(self) -> ProviderInfo:
        cls = type(self)
        if not cls.__provider_info__:
            cls.__provider_info__ = ProviderInfo.resolve()
        return cls.__provider_info__

    @classmethod
    def provider_cls(cls):
        if not cls.__provider_info__:
            cls.__provider_info__ = ProviderInfo.resolve()

        return next(
            klazz
            for klazz in cls.__subclasses__()
            if klazz.__module__.startswith(cls.__provider_info__.module)
        )

    @classmethod
    def reset_provider(cls):
        cls.__provider_info__ = None
