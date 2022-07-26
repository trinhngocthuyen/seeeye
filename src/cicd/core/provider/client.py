from typing import Optional, Union

from cicd.core.client import Client
from cicd.core.mixin.provider import ProviderMixin

ID = Union[int, str]


class ProviderClient(Client, ProviderMixin):
    def get_projects(self, **kwargs):
        raise NotImplementedError

    def get_project(self, identifier: ID, **kwargs):
        raise NotImplementedError

    def get_pull_requests(
        self, project_identifier: ID, state: Optional[str] = None, **kwargs
    ):
        raise NotImplementedError

    def get_pull_request(self, project_identifier: ID, identifier: ID, **kwargs):
        raise NotImplementedError
