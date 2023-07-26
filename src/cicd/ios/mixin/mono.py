from .archive import ArchiveMixin
from .build import BuildMixin
from .cov import CovMixin
from .test import TestMixin


class MonoMixin(
    ArchiveMixin,
    BuildMixin,
    TestMixin,
    CovMixin,
):
    pass
