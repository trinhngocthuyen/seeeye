import typing as t

from cicd.ios.simulator import Simulator


class SimulatorMixin:
    simulator: t.Optional[Simulator] = None

    def prepare_simulator(self, **kwargs):
        destination = kwargs.get('destination')
        if destination:
            self.simulator = Simulator.from_xcodebuild_destination(destination)
        else:
            self.simulator = Simulator(**kwargs)
        if self.simulator:
            with self.simulator:
                pass
