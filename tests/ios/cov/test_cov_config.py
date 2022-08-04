import pytest

from cicd.ios.cov.config import CovConfig


@pytest.fixture
def sut(cov_config):
    return cov_config


def test_cov_config(sut: CovConfig):
    assert sut.targets == ['A1.app', 'A2.app']
    assert sut.ignore == ['*.generated.*', 'src/ignored/*']
    assert sut.path_mapping == {'from': r'^\S+\/project\/', 'to': ''}
