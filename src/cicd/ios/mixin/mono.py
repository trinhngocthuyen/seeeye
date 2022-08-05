from .build import BuildMixin
from .cov import CovMixin
from .test import TestMixin


class MonoMixin(
    BuildMixin,
    TestMixin,
    CovMixin,
):
    pass
