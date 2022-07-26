from cicd.core.provider.client import ID

from .base import ProviderModel, model
from .project import Project


class API(ProviderModel):
    @model(Project, to_list=True)
    def get_projects(self, **kwargs):
        return self.client.get_projects(**kwargs)

    @model(Project)
    def get_project(self, identifier: ID, **kwargs):
        return self.client.get_project(identifier=identifier, **kwargs)
