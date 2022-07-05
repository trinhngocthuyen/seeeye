from typing import Optional

from cicd.ios.runner.xcodebuild import XCBBuildRunner


class BuildMixin:
    def start_building(self, **kwargs):
        runner = XCBBuildRunner()
        runner.run(**kwargs)
