from functools import cached_property, wraps
from typing import Any, Callable, List, Literal, Type, TypeVar, overload

from typing_extensions import ParamSpec

from cicd.core.mixin.provider import ProviderMixin
from cicd.core.provider.client import ProviderClient

D = TypeVar('D')
P = ParamSpec('P')


class ProviderModel(dict, ProviderMixin):
    __desc__ = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ds = args[0] if args else kwargs
        for k in getattr(self, '__annotations__', {}):
            if k.startswith('__') and k.endswith('__'):
                continue
            field = self.schema.get(k, k)
            setattr(self, k, ds.get(field))

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


@overload
def model(
    dtype: Type[D], to_list: Literal[True]
) -> Callable[[Callable[P, Any]], Callable[P, List[D]]]:
    ...


@overload
def model(
    dtype: Type[D], to_list: Literal[False] = False
) -> Callable[[Callable[P, Any]], Callable[P, D]]:
    ...


def model(
    dtype: Type[D],
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
                return [dtype(x) for x in raw]
            return dtype(raw)

        return wrapper

    return decorator
