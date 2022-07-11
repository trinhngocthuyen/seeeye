from cicd.ios.runner.xcodebuild import XCBTestRunner

from .simulator import SimulatorMixin


class TestMixin(SimulatorMixin):
    def start_testing(self, **kwargs):
        self.prepare_simulator(destination=kwargs.get('destination'))
        runner = XCBTestRunner()
        runner.run(**kwargs)
