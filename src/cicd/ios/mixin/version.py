import re
import typing as t

from cicd.core.logger import logger
from cicd.core.version import Version

from .project import MetadataMixin

T = t.TypeVar('T')


class VersionMixin(MetadataMixin):
    def _from_build_settings(self, key, dtype: t.Type[T]) -> T:
        content = self.metadata.pbxproj_path.read_text()
        return max(dtype(x) for x in re.findall(f'\\b{key} = (.*);', content))

    def _update_build_settings(self, key, value):
        content = self.metadata.pbxproj_path.read_text()
        content = re.sub(f'\\b{key} = (.*);', f'{key} = {value};', content)
        self.metadata.pbxproj_path.write_text(content)

    @property
    def version(self) -> Version:
        return self._from_build_settings(key='MARKETING_VERSION', dtype=Version)

    @property
    def build_number(self) -> int:
        return self._from_build_settings(key='CURRENT_PROJECT_VERSION', dtype=int)

    def bump(self, **kwargs):
        if kwargs.get('version') or kwargs.get('version_next'):
            self.bump_version(to_value=kwargs.get('version'))
        if kwargs.get('build_number') or kwargs.get('build_number_next'):
            self.bump_build_number(to_value=kwargs.get('build_number'))

    def bump_version(self, to_value: t.Optional[str] = None) -> Version:
        to_value = Version(to_value) if to_value else self.version.next()
        logger.info(f'Bump version to: {to_value}')
        self._update_build_settings(key='MARKETING_VERSION', value=str(to_value))
        return to_value

    def bump_build_number(self, to_value: t.Optional[int] = None) -> int:
        to_value = to_value or (self.build_number + 1)
        logger.info(f'Bump build number to: {to_value}')
        self._update_build_settings(key='CURRENT_PROJECT_VERSION', value=to_value)
        return to_value
