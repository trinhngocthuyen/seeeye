import typing as t

from cicd.core.provider.client import ID, ProviderClient


class GithubClient(ProviderClient):
    BASE_URL = 'https://api.github.com'

    def get_projects(self, **kwargs):
        return self.request(endpoint='/repositories', **kwargs)

    def get_project(self, identifier: ID, **kwargs):
        return self.request(endpoint=f'/repos/{identifier}', **kwargs)

    def get_pull_requests(
        self, project_identifier: ID, state: t.Optional[str] = None, **kwargs
    ):
        params = kwargs.pop('params', {})
        if state is not None:
            params['state'] = state
        return self.request(
            endpoint=f'/repos/{project_identifier}/pulls', params=params, **kwargs
        )

    def get_pull_request(self, project_identifier: ID, identifier: ID, **kwargs):
        return self.request(
            endpoint=f'/repos/{project_identifier}/pulls/{identifier}', **kwargs
        )
