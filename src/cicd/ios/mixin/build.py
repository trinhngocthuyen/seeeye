from cicd.ios.runner.xcodebuild import XCBBuildRunner

from .base_ios import BaseIOSMixin


class BuildMixin(BaseIOSMixin):
    def start_building(self):
        with self.step('pre-run'):
            self.pre_run()

        with self.step('run'):
            runner = XCBBuildRunner()
            runner.run(**self.kwargs)

        with self.step('post-run'):
            self.post_run()
