from cicd.core.utils.step import step


class StepMixin:
    '''A mixin that provides contextual logs including time spent
    of the tasks under under the same context.
    '''

    def step(self, name: str, **kwargs):
        return step(name=name, **kwargs)
