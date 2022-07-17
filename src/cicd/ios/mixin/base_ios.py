from cicd.core.mixin.base import BaseMixin

from .cocoapods import CocoaPodsMixin
from .simulator import SimulatorMixin


class BaseIOSMixin(
    BaseMixin,
    SimulatorMixin,
    CocoaPodsMixin,
):
    def pre_run(self, **kwargs):
        self.prepare_cocoapods(**kwargs)
        self.prepare_simulator(**kwargs)

    def post_run(self, **kwargs):
        pass
