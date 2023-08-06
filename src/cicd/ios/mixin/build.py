from cicd.ios.actions.xcodebuild import XCBBuildAction

from .base_ios import BaseIOSMixin


class BuildMixin(BaseIOSMixin):
    def start_building(self):
        self.runner_exec(action_cls=XCBBuildAction)
