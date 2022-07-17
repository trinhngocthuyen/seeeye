from cicd.core.utils.step import step


class StepMixin:
    def step(self, name: str, **kwargs):
        return step(name=name, **kwargs)
