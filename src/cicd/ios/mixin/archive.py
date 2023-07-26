from cicd.ios.runner.xcodebuild import XCBArchiveRunner

from .base_ios import BaseIOSMixin


class ArchiveMixin(BaseIOSMixin):
    def start_archiving(self):
        with self.step('pre-run'):
            self.pre_run()

        with self.step('run'):
            runner = XCBArchiveRunner()
            runner.run(**self.kwargs)

        with self.step('post-run'):
            self.post_run()
