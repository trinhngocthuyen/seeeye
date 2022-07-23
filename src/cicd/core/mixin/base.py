from .git import GitMixin
from .logger import LoggerMixin
from .step import StepMixin


class BaseMixin(
    LoggerMixin,
    GitMixin,
    StepMixin,
):
    pass
