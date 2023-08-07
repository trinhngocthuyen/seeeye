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
                self.logger.info(
                    'Profiles mapping was not specified. Will resolve from build settings'
                )
                build_settings = self.project.resolve_build_settings(
                    action='archive', **self.kwargs
                )
                bundle_id = build_settings.get('PRODUCT_BUNDLE_IDENTIFIER')
                profile = build_settings.get('PROVISIONING_PROFILE_SPECIFIER')
                return {bundle_id: profile} if bundle_id and profile else {}
            return dict([tuple(kv.split(':')) for kv in profiles.split(',')])

        mapping = profiles_mapping()
        if not mapping:
            self.logger.warning(
                'Profiles mapping is empty. This usually results in error when exporting to the ipa. '
                'Consider specifying `PROVISIONING_PROFILE_SPECIFIER` in the build settings '
                'or using the `--profiles` in the CLI.'
            )
        return {
            'method': self.kwargs.get('export_method') or 'app-store',
            'provisioningProfiles': mapping,
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
