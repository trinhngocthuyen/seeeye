from typing import Dict, List, Optional

from cicd.core.syntax.yaml import YAML


class CovConfig(YAML):
    @property
    def targets(self) -> List[str]:
        return self.query('targets')

    @property
    def ignore(self) -> List[str]:
        return self.query('ignore')

    @property
    def path_mapping(self) -> Optional[Dict[str, str]]:
        return self.query('path_mapping')
