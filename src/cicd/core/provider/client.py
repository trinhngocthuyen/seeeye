import typing as t

from cicd.core.client import Client
from cicd.core.mixin.provider import ProviderMixin

ID = t.Union[int, str]


class ProviderClient(Client, ProviderMixin):
    '''An abstract client for CI provider APIs.'''

    def get_projects(self, **kwargs):
        '''Get the list of (public) projects.'''
        raise NotImplementedError

    def get_project(self, identifier: ID, **kwargs):
        '''Get the details of a project.

        :param identifier: The identifier of the project.
        '''
        raise NotImplementedError

    def get_pull_requests(
        self, project_identifier: ID, state: t.Optional[str] = None, **kwargs
    ):
        '''Get the pull/merge requests of the given project.

        :param project_identifier: The identifier of the project.
        :param state: The state (ex. open/closed/all) of the pull/merge requests.
        '''
        raise NotImplementedError

    def get_pull_request(self, project_identifier: ID, identifier: ID, **kwargs):
        '''Get the details of a pull/merge request.

        :param project_identifier: The identifier of the project.
        :param identifier: The identifier of the pull/merge request.
        '''
        raise NotImplementedError
