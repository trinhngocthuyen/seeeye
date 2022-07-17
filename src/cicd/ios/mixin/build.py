from cicd.ios.runner.xcodebuild import XCBBuildRunner

from .base_ios import BaseIOSMixin


class BuildMixin(BaseIOSMixin):
    def start_building(self, **kwargs):
        with self.step('pre-run'):
            self.pre_run(**kwargs)

        with self.step('run'):
            runner = XCBBuildRunner()
            runner.run(**kwargs)

        with self.step('post-run'):
            self.post_run(**kwargs)
