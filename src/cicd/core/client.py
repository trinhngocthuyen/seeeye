from typing import Any, Dict, Optional, Type, TypeVar

import requests

D = TypeVar('D', bound=dict)
T = TypeVar('T', bound='Client')


class Client:
    BASE_URL: Optional[str] = None
    token: Optional[str] = None

    def __new__(cls):
        if hasattr(cls, 'instance') and isinstance(getattr(cls, 'instance'), cls):
            return cls.instance
        cls.instance = super(Client, cls).__new__(cls)
        return cls.instance

    def config(
        self: T, base_url: Optional[str] = None, token: Optional[str] = None, **kwargs
    ) -> T:
        if base_url:
            self.BASE_URL = base_url
        if token:
            self.token = token
        return self

    def make_headers(self) -> Dict[str, Any]:
        headers = {}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers

    def make_paging_params(self, paging) -> Dict[str, Any]:
        if isinstance(paging, int):
            return {'page': 1, 'per_page': paging}
        if isinstance(paging, (tuple, list)):
            return {'page': paging[0], 'per_page': paging[1]}
        return {}

    def request(
        self,
        endpoint: str,
        method: str = 'get',
        as_type: Optional[Type[D]] = None,
        to_list: bool = False,
        **kwargs,
    ) -> Optional[D]:
        url = f'{self.BASE_URL}{endpoint}'
        headers = {**self.make_headers(), **kwargs.pop('headers', {})}
        params = kwargs.pop('params', {})
        paging = kwargs.pop('paging', None)
        if paging:
            params.update(self.make_paging_params(paging))
        response = requests.request(
            url=url, method=method, headers=headers, params=params, **kwargs
        )
        response.raise_for_status()
        try:
            raw = response.json()
        except requests.exceptions.JSONDecodeError:
            raw = response.content.decode('utf-8')
        if as_type:
            if to_list:
                return [as_type(x) for x in raw]
            return as_type(raw)
        return raw
