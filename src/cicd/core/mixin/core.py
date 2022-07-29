from .git import GitMixin
from .logger import LoggerMixin
from .step import StepMixin


class CoreMixin(
    LoggerMixin,
    GitMixin,
    StepMixin,
):
    pass
