from cicd.ios.runner.xcodebuild import XCBBuildRunner

from .base_ios import BaseIOSMixin


class BuildMixin(BaseIOSMixin):
    def start_building(self, **kwargs):
        self.pre_run(**kwargs)
        runner = XCBBuildRunner()
        runner.run(**kwargs)
        self.post_run(**kwargs)
