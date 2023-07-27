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

    ipa_path: t.Optional[Path]
    dsym_path: t.Optional[Path]

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
        cmd = XCBExportCmdMaker(
            archive_path=self.xcarchive_path,
            export_options_plist=plist_path,
            export_path=in_dir,
        ).make()
        sh.exec(cmd, capture_output=False, log_cmd=True)
        self.ipa_path = self._collect(from_dir=in_dir, pattern='*.ipa')[0]

    def zip_dsyms(self, in_dir: Path):
        cmd = 'cd {} && zip -r {} *.dSYM'.format(
            sh.quote(self.xcarchive_path / 'dSYMs'),
            sh.quote(in_dir / f'{self.ipa_path.stem}.app.dSYM.zip'),
        )
        sh.exec(cmd, capture_output=False, log_cmd=True)
        dsym_paths = self._collect(from_dir=in_dir, pattern='*.dSYM.zip')
        self.dsym_path = dsym_paths[0] if dsym_paths else None

    def _collect(self, from_dir: Path, pattern: str):
        export_path = Path(self.kwargs.get('export_path') or '.')
        return [FileUtils.copy(p, export_path) for p in from_dir.glob(pattern)]
