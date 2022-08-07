import re
import typing as t
from fnmatch import fnmatch
from functools import cached_property
from pathlib import Path

from cicd.core.syntax.json import JSON

from .config import CovConfig


class CovReport:
    def __init__(
        self, raw: t.Union[JSON, t.Dict[str, t.Any]], config: CovConfig
    ) -> None:
        self.raw = raw
        self.config = config

    @cached_property
    def targets_data(self):
        def chosen(target) -> bool:
            if self.config.targets:
                return target['name'] in self.config.targets
            return True

        return [target for target in self.raw['targets'] if chosen(target)]

    @cached_property
    def files_data(self):
        def shorten(path: str) -> str:
            mapping = self.config.path_mapping
            if mapping:
                return re.sub(mapping['from'], mapping['to'], path)
            return path

        def chosen(fname) -> bool:
            if self.config.ignore:
                return not any(fnmatch(fname, p) for p in self.config.ignore)
            return True

        result = []
        for target in self.targets_data:
            for item in target['files']:
                path = shorten(item['path'])
                if chosen(path):
                    result.append({**item, 'path': path})
        return result

    @cached_property
    def total_coverage(self) -> float:
        total_covered_lines = sum(x['coveredLines'] for x in self.files_data)
        total_executable_lines = sum(x['executableLines'] for x in self.files_data)
        return total_covered_lines / max(1, total_executable_lines)

    @cached_property
    def breakdown_data(self) -> t.Dict[str, t.Any]:
        return {}  # TODO: Implement this

    @property
    def summary_data(self) -> t.Dict[str, t.Any]:
        return {
            'coverage': self.total_coverage,
        }

    @property
    def details_data(self) -> t.Dict[str, t.Any]:
        return {
            'files': self.files_data,
        }

    def export(self, path: t.Union[str, Path]):
        exported_data = {
            'summary': self.summary_data,
            'breakdown': self.breakdown_data,
            'details': self.details_data,
        }
        JSON(data=exported_data).save(path=path)
