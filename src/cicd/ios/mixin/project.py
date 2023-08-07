from cicd.ios.project.metadata import Metadata
from cicd.ios.project.project import Project

__all__ = ['MetadataMixin', 'ProjectMixin']

_metadata = Metadata()
_project = Project(metadata=_metadata)


class MetadataMixin:
    @property
    def metadata(self):
        return _metadata


class ProjectMixin(MetadataMixin):
    @property
    def project(self):
        return _project
