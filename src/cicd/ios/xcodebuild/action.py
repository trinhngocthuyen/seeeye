import subprocess
from shlex import quote
from typing import Any, Dict, List, Optional, Union

from cicd.core.logger import logger
from cicd.ios.project.metadata import Metadata

__all__ = ['XCBAction']


class CmdMaker:
    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs
        self.metadata = Metadata()

    def make(self) -> Optional[str]:
        raise NotImplementedError

    def quote(self, s) -> Optional[str]:
        return quote(str(s)) if s is not None else None


class XCBCmdMaker(CmdMaker):
    def make(self) -> Optional[str]:
        xctestrun = self.kwargs.get('xctestrun')
        workspace = self.kwargs.get('workspace')
        scheme = self.kwargs.get('scheme')
        project = self.kwargs.get('project')
        target = self.kwargs.get('target')
        if xctestrun:
            workspace, scheme = None, None
            project, target = None, None
        elif workspace or scheme:
            workspace = workspace or self.metadata.xcworkspace_path  # prefill
            scheme = scheme or self.metadata.scheme  # prefill
            project, target = None, None
        elif project or target:
            # TODO: prefill target?
            project = project or self.metadata.xcodeproj_path  # prefill
            workspace, scheme = None, None
        elif self.metadata.xcworkspace_path:
            workspace = self.metadata.xcworkspace_path
            scheme = self.metadata.scheme
        elif self.metadata.xcodeproj_path:
            project = self.metadata.xcodeproj_path

        default_destination = 'platform=iOS Simulator,name=iPhone 8'
        xcb_kwargs = {
            'derivedDataPath': self.kwargs.get('derived_data_path'),
            'xctestrun': xctestrun,
            'workspace': workspace,
            'scheme': scheme,
            'project': project,
            'target': target,
            'configuration': self.kwargs.get('configuration'),
            'sdk': self.kwargs.get('sdk'),
            'destination': self.kwargs.get('destination') or default_destination,
        }
        xcargs = self.kwargs.get('xcargs', {})
        actions = self.kwargs.get('actions', [])
        if self.kwargs.get('clean'):
            actions.insert(0, 'clean')

        cmps = ['xcodebuild'] + actions
        cmps += [
            x
            for (k, v) in xcb_kwargs.items()
            for x in [f'-{k}', self.quote(v)]
            if v is not None
        ]
        if isinstance(xcargs, str):
            cmps += [xcargs]
        elif isinstance(xcargs, (tuple, list)):
            cmps += list(xcargs)
        elif isinstance(xcargs, dict):
            cmps += [f'{k}={quote(v)}' for (k, v) in xcargs.items()]
        return ' '.join(cmps)


class LogCmdMaker(CmdMaker):
    def make(self) -> Optional[str]:
        return self.kwargs.get('log_formatter') or self.metadata.resolve_program(
            'xcpretty'
        )


class TeeCmdMaker(CmdMaker):
    def make(self) -> Optional[str]:
        log_path = self.kwargs.get('log_path')
        if log_path:
            return f'tee {quote(log_path)}'


class XCBAction:
    def run(self, **kwargs):
        makers = [
            XCBCmdMaker(**kwargs),
            LogCmdMaker(**kwargs),
            TeeCmdMaker(**kwargs),
        ]
        cmd = ' | '.join(x for x in [maker.make() for maker in makers] if x)
        logger.info(f'$ {cmd}')
        subprocess.run(cmd, check=True, shell=True)


class XCBBuildAction(XCBAction):
    def run(self, **kwargs):
        if not kwargs.get('actions'):
            kwargs['actions'] = ['build']
        return super().run(**kwargs)


class XCBTestAction(XCBAction):
    def run(self, **kwargs):
        if not kwargs.get('actions'):
            kwargs['actions'] = ['test']
        return super().run(**kwargs)
