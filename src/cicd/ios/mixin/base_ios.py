from cicd.core.mixin.core import CoreMixin

from .cocoapods import CocoaPodsMixin
from .simulator import SimulatorMixin


class BaseIOSMixin(
    CoreMixin,
    SimulatorMixin,
    CocoaPodsMixin,
):
    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs
        super().__init__()

    def pre_run(self):
        self.prepare_cocoapods(**self.kwargs)
        if self.kwargs.get('prepare_simulator', True):
            self.prepare_simulator(**self.kwargs)
            # Workaround: For children to use simulator info
            self.kwargs['_simulator'] = self.simulator

    def post_run(self):
        pass
