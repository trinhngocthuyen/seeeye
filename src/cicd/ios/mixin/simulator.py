from cicd.ios.simulator import Simulator


class SimulatorMixin:
    def prepare_simulator(self, **kwargs):
        destination = kwargs.get('destination')
        if destination:
            simulator = Simulator.from_xcodebuild_destination(destination)
        else:
            simulator = Simulator(**kwargs)
        if simulator:
            with simulator:
                pass
