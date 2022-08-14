import typing as t
from functools import cached_property

from cicd.core.provider.info import ProviderInfo

T = t.TypeVar('T', bound='ProviderMixin')


class ProviderMixin:
    '''A mixin that provides helpers to resolve the responsible class
    corresponding to the current CI provider.

    In the following example, ``Env`` is a ``ProviderMixin``. When running in Github Actions, ``Env``'s provider is resolved to ``GithubEnv``.

    >>> class Env(ProviderMixin):
    >>>     ...
    >>> class GithubEnv(Env): # in cicd.providers.github.env
    >>>     ...
    >>> class GitlabEnv(Env): # in cicd.providers.gitlab.env
    >>>     ...

    :notes: Use this mixin on the abstract class, not the concrete class.
    '''

    __provider_info__: t.Optional[ProviderInfo] = None

    @cached_property
    def provider(self: T) -> T:
        '''Resolve the object of the corresponding provider-class.'''
        return self.provider_cls()()

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
