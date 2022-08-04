import pytest

from cicd.ios.cov import CovReport


@pytest.fixture
def sut(cov_report):
    return cov_report


def test_cov_report(sut: CovReport):
    assert sut.total_coverage == 0.25
