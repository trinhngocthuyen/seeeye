import typing as t

from cicd.core.mixin.core import CoreMixin
from cicd.ios.actions.base import Action
from cicd.ios.runner.base import Runner

from .cocoapods import CocoaPodsMixin
from .simulator import SimulatorMixin
from .version import VersionMixin


class BaseIOSMixin(
    CoreMixin,
    SimulatorMixin,
    CocoaPodsMixin,
    VersionMixin,
):
    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs
        self.runner = Runner()
        super().__init__()

    def runner_exec(self, action_cls: t.Type[Action]):
        with self.step('pre-run'):
            self.pre_run()

        with self.step('run'):
            self.runner.run(action_cls=action_cls, **self.kwargs)

        with self.step('post-run'):
            self.post_run()

    def pre_run(self):
        self.prepare_cocoapods(**self.kwargs)
        self.bump(**self.kwargs)
        if self.kwargs.get('prepare_simulator', True):
            self.prepare_simulator(**self.kwargs)
            # Workaround: For children to use simulator info
            self.kwargs['_simulator'] = self.simulator

    def post_run(self):
        pass
