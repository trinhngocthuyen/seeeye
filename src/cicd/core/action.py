from cicd.core.mixin.core import CoreMixin


class Action(CoreMixin):
    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs

    def run(self):
        pass
