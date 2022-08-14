import typing as t

import requests

D = t.TypeVar('D', bound=dict)
T = t.TypeVar('T', bound='Client')


class Client:
    '''Base class that provides building blocks for API wrappers.

    Clients are per-class singletons.
    '''

    BASE_URL: t.Optional[str] = None
    token: t.Optional[str] = None

    def __new__(cls):
        if hasattr(cls, 'instance') and isinstance(getattr(cls, 'instance'), cls):
            return cls.instance
        cls.instance = super(Client, cls).__new__(cls)
        return cls.instance

    def config(
        self: T,
        base_url: t.Optional[str] = None,
        token: t.Optional[str] = None,
        **kwargs,
    ) -> T:
        '''Config the client.

        :param base_url: The base url of the APIs.
        :param token: The API token used in each request.
        :return: The current client.
        '''
        if base_url:
            self.BASE_URL = base_url
        if token:
            self.token = token
        return self

    def make_headers(self) -> t.Dict[str, t.Any]:
        '''Make up headers for each requests.

        Subclasses override this function to append/modify request headers.
        '''

        headers = {}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers

    def make_paging_params(
        self,
        paging: t.Union[int, t.Tuple[int, int], t.List[int]],
    ) -> t.Dict[str, t.Any]:
        '''Make up paging params for request params.'''

        if isinstance(paging, int):
            return {'page': 1, 'per_page': paging}
        if isinstance(paging, (tuple, list)):
            return {'page': paging[0], 'per_page': paging[1]}
        return {}

    def request(
        self,
        endpoint: str,
        method: str = 'get',
        as_type: t.Optional[t.Type[D]] = None,
        to_list: bool = False,
        **kwargs,
    ) -> t.Optional[D]:
        '''Make an API request.

        :param endpoint: The API endpoint.
        :param method: The request method (default as ``get``).
        :param as_type: The model to which the raw content should be converted.
        :param to_list: Whether the return value should be a list, used together with ``as_type``.
        :return: The model/list of models (if ``as_type`` is specified),
            or the json content, or the raw content.
        '''

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
