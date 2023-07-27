import plistlib
import typing as t
from pathlib import Path

from cicd.core.utils.file import FileUtils
from cicd.core.utils.sh import sh
from cicd.ios.actions.xcodebuild.base import CmdMaker

from .base import XCBAction


class ArchiveError(Exception):
    pass


class XCBArchiveAction(XCBAction):
    '''A class that interacts with the xcodebuild command, particularly for archive actions.'''

    ipa_path: t.Optional[Path] = None
    dsym_path: t.Optional[Path] = None

    def run(self):
        kwargs = self.kwargs
        try:
            if not kwargs.get('actions'):
                kwargs['actions'] = ['archive']
            with self.collect_xcarchives():
                super().run()

            with FileUtils.tempdir() as dir:
                with self.step('Export ipa'):
                    self.export_ipa(in_dir=dir)
                with self.step('Zip dSYMs'):
                    self.zip_dsyms(in_dir=dir)
                self.logger.info(
                    f'Output: ipa: {self.ipa_path}, dsym: {self.dsym_path}'
                )
        except Exception as e:
            raise ArchiveError(e)

    def export_options(self) -> t.Dict[str, t.Any]:
        def profiles_mapping() -> t.Dict[str, t.Any]:
            profiles = self.kwargs.get('profiles')
            if not profiles:
                return {}
            return dict([tuple(kv.split(':')) for kv in profiles.split(',')])

        return {
            'method': self.kwargs.get('export_method') or 'app-store',
            'provisioningProfiles': profiles_mapping(),
        }

    def export_ipa(self, in_dir: Path):
        class XCBExportCmdMaker(CmdMaker):
            def make(self) -> t.Optional[str]:
                cmps = ['xcodebuild', '-exportArchive'] + self.args_from_dict(
                    {
                        'archivePath': self.kwargs.get('archive_path'),
                        'exportOptionsPlist': self.kwargs.get('export_options_plist'),
                        'exportPath': self.kwargs.get('export_path'),
                    }
                )
                return ' '.join(cmps)

        plist_path = in_dir / 'export_options.plist'
        plist_path.write_bytes(plistlib.dumps(self.export_options()))
        self.logger.debug(
            'Generate export options plist:'
            '\n-------------------------\n'
            f'{plist_path.read_text()}'
            '\n-------------------------\n'
        )
        cmd = XCBExportCmdMaker(
            archive_path=self.xcarchive_path,
            export_options_plist=plist_path,
            export_path=in_dir,
        ).make()
        sh.exec(cmd, log_cmd=True)
        self.ipa_path = self._collect(from_dir=in_dir, pattern='*.ipa')[0]

    def zip_dsyms(self, in_dir: Path):
        if not list(self.xcarchive_path.glob('dSYMs/*')):
            self.logger.warning('No dsym detected in the xcarchive')
            return

        cmd = 'cd {} && zip -r {} *.dSYM'.format(
            sh.quote(self.xcarchive_path / 'dSYMs'),
            sh.quote(in_dir / f'{self.ipa_path.stem}.app.dSYM.zip'),
        )
        sh.exec(cmd, log_cmd=True)
        self.dsym_path = self._collect(from_dir=in_dir, pattern='*.dSYM.zip')[0]

    def _collect(self, from_dir: Path, pattern: str):
        output_path = Path(self.kwargs.get('output-path') or '.')
        return [FileUtils.copy(p, output_path) for p in from_dir.glob(pattern)]
