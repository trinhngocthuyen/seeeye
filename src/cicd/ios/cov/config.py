import typing as t

from cicd.core.syntax.yaml import YAML


class CovConfig(YAML):
    @property
    def targets(self) -> t.List[str]:
        return self.query('targets')

    @property
    def ignore(self) -> t.List[str]:
        return self.query('ignore')

    @property
    def path_mapping(self) -> t.Optional[t.Dict[str, str]]:
        return self.query('path_mapping')
