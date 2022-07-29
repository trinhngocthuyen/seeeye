from cicd.core.mixin.core import CoreMixin

from .cocoapods import CocoaPodsMixin
from .simulator import SimulatorMixin


class BaseIOSMixin(
    CoreMixin,
    SimulatorMixin,
    CocoaPodsMixin,
):
    def pre_run(self, **kwargs):
        self.prepare_cocoapods(**kwargs)
        self.prepare_simulator(**kwargs)

    def post_run(self, **kwargs):
        pass
