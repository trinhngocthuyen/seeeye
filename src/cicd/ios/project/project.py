import typing as t

from cicd.core.utils.sh import sh

from .build_settings import BuildSettings
from .metadata import Metadata


class Project:
    def __init__(self, metadata: t.Optional[Metadata] = None) -> None:
        self.metadata = metadata or Metadata()

    def resolve_build_settings(self, **kwargs) -> BuildSettings:
        def unpack(cmps, *keys):
            for key in keys:
                if value := kwargs.get(key):
                    cmps += [f'-{key}', sh.quote(str(value))]

        cmps = ['xcodebuild', '-showBuildSettings']
        unpack(cmps, 'configuration', 'scheme', 'project', 'workspace', 'target')
        if action := kwargs.get('action'):
            cmps.append(action)
        cmd = ' '.join(cmps)
        raw = sh.exec(cmd, capture_output=True, log_cmd=True)
        return BuildSettings.from_xcodebuild_settings(raw)
