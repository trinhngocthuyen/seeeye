from cicd.ios.project.metadata import Metadata

__all__ = ['MetadataMixin']

_metadata = Metadata()


class MetadataMixin:
    @property
    def metadata(self):
        return _metadata
