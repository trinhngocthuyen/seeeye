from cicd.ios.actions.xcodebuild import XCBArchiveAction

from .base_ios import BaseIOSMixin


class ArchiveMixin(BaseIOSMixin):
    def start_archiving(self):
        self.kwargs['prepare_simulator'] = False
        self.runner_exec(action_cls=XCBArchiveAction)
