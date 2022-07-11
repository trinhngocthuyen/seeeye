from cicd.ios.runner.xcodebuild import XCBBuildRunner

from .simulator import SimulatorMixin


class BuildMixin(SimulatorMixin):
    def start_building(self, **kwargs):
        self.prepare_simulator(destination=kwargs.get('destination'))
        runner = XCBBuildRunner()
        runner.run(**kwargs)
