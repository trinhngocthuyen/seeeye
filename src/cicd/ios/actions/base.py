from functools import cached_property
from pathlib import Path

from cicd.core.action import Action
from cicd.ios.mixin.metadata import MetadataMixin


class IOSAction(Action, MetadataMixin):
    @cached_property
    def derived_data_path(self) -> Path:
        path = self.kwargs.get('derived_data_path')
        return Path(path) if path else self.metadata.default_derived_data_path
