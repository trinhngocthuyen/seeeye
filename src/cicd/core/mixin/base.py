from .logger import LoggerMixin
from .step import StepMixin


class BaseMixin(
    LoggerMixin,
    StepMixin,
):
    pass
