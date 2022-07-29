from shlex import quote
from typing import Optional

from cicd.core.utils.sh import sh
from cicd.ios.actions.base import IOSAction
from cicd.ios.mixin.metadata import MetadataMixin

__all__ = ['XCBAction']


class CmdMaker(MetadataMixin):
    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs

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
        tests = self.kwargs.get('only_testing', [])
        if self.kwargs.get('clean'):
            actions.insert(0, 'clean')

        cmps = ['xcodebuild'] + actions
        cmps += [
            x
            for (k, v) in xcb_kwargs.items()
            for x in [f'-{k}', self.quote(v)]
            if v is not None
        ]
        cmps += [x for test in tests for x in ['-only-testing', test]]
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


class XCBAction(IOSAction, MetadataMixin):
    '''A class that interacts with the xcodebuild command.

    It is up to subclasses to guarantee params are passed valid.
    For example, ``only_testing`` and ``build_for_testing`` should not co-exist.
    When both are declared, the action is not responsible for choosing which one should be picked up.

    :param workspace: Path to the ``.xcworkspace`` file.
    :param project: Path to the ``.xcodeproj`` file.
    :param xctestrun: Path to the xctestrun bundle.
    :param target: Target to build.
    :param scheme: Scheme.
    :param configuration: The configuration (ex. Debug/Release).
    :param derived_data_path: The derived data path.
    :param sdk: The sdk (ex. iphonesimulator).
    :param destination: The destination (ex. "platform=iOS Simulator,name=EX").
    :param clean: Whether to do a clean build/test.
    :param only_testing: The list of tests to execute.
    :param actions: The actions (clean, build, test, archive, profile...).
    :param xcargs: The overriden build settings. Can be a str, list, or dict. Examples: ``"ONLY_ACTIVE_ARCH=YES"``, ``["ONLY_ACTIVE_ARCH=YES", "DEBUG_INFORMATION_FORMAT=dwarf"]``, ``{"ONLY_ACTIVE_ARCH": "YES", "DEBUG_INFORMATION_FORMAT": "dward"}``
    '''

    def run(self):
        '''Execute the action'''

        kwargs = self.kwargs
        makers = [
            XCBCmdMaker(**kwargs),
            TeeCmdMaker(**kwargs),
            LogCmdMaker(**kwargs),
        ]
        cmd = 'set -o pipefail && '
        cmd += ' | '.join(x for x in [maker.make() for maker in makers] if x)
        return sh.exec(
            cmd, timeout=kwargs.get('timeout'), capture_output=False, log_cmd=True
        )
