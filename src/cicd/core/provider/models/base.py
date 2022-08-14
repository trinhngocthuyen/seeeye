import typing as t
from functools import cached_property, wraps

from pydantic import BaseModel
from typing_extensions import ParamSpec

from cicd.core.mixin.provider import ProviderMixin
from cicd.core.provider.client import ProviderClient

D = t.TypeVar('D')
P = ParamSpec('P')


class ProviderModel(BaseModel, ProviderMixin):
    __desc__ = []

    class Config:
        # Workaround for cached_property
        # Ref: https://github.com/pydantic/pydantic/issues/2763#issuecomment-835725898
        keep_untouched = (cached_property,)

    def __str__(self) -> str:
        return '{} {}'.format(
            self.__class__.__name__,
            ' '.join(f'({getattr(self, k)})' for k in self.__desc__),
        )

    def __repr__(self) -> str:
        return self.__str__()

    @cached_property
    def client(self) -> ProviderClient:
        return ProviderClient().provider

    @property
    def schema(self):
        return {}


@t.overload
def model(
    dtype: t.Type[D], to_list: t.Literal[True]
) -> t.Callable[[t.Callable[P, t.Any]], t.Callable[P, t.List[D]]]:
    ...


@t.overload
def model(
    dtype: t.Type[D], to_list: t.Literal[False] = False
) -> t.Callable[[t.Callable[P, t.Any]], t.Callable[P, D]]:
    ...


def model(
    dtype: t.Type[D],
    to_list: bool = False,
):
    '''A decorator to convert json data to model/list of models.

    .. code-block:: python

        class Model:
            @model(Project, to_list=True)
            def get_projects(self):
                ...

            @model(Project)
            def get_project(self):
                ...
    '''

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            raw = func(*args, **kwargs)
            if to_list:
                return [dtype(**x) for x in raw]
            return dtype(**raw)

        return wrapper

    return decorator
