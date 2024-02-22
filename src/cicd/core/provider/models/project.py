from .base import ProviderModel, model
from .pr import PullRequest


class Project(ProviderModel):
    __desc__ = ['id', 'name']

    id: int | None
    name: str | None
    description: str | None
    full_name: str | None

    @property
    def url(self) -> str:
        return self.get('html_url', self.get('web_url'))

    @property
    def identifier(self) -> int | str:
        if self.provider_info.name == 'github':
            return self.full_name
        return self.id

    @model(PullRequest, to_list=True)
    def get_pull_requests(self, state: str | None = None, **kwargs):
        return self.client.get_pull_requests(
            project_identifier=self.identifier, state=state, **kwargs
        )

    @model(PullRequest)
    def get_pull_request(self, identifier, **kwargs):
        return self.client.get_pull_request(
            project_identifier=self.identifier, identifier=identifier, **kwargs
        )
