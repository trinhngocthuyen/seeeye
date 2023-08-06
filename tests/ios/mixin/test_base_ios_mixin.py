import pytest

from cicd.ios.mixin.base_ios import BaseIOSMixin


@pytest.fixture
def sut_kwargs():
    return {}


@pytest.fixture
def sut(sut_kwargs, bag, monkeypatch):
    this = BaseIOSMixin(**sut_kwargs)
    monkeypatch.setattr(this, 'pod_install', bag.pod_install)
    monkeypatch.setattr(this, 'prepare_simulator', bag.prepare_simulator)
    monkeypatch.setattr(this, 'bump_version', bag.bump_version)
    monkeypatch.setattr(this, 'bump_build_number', bag.bump_build_number)
    return this


@pytest.mark.parametrize('sut_kwargs', [{'foo': 'bar'}])
def test_retain_params(sut: BaseIOSMixin, sut_kwargs):
    assert sut.kwargs == sut_kwargs


def test_pre_run_without_params(sut: BaseIOSMixin, bag):
    sut.pre_run()
    bag.pod_install.assert_not_called()
    bag.prepare_simulator.assert_called()
    bag.bump_version.assert_not_called()
    bag.bump_build_number.assert_not_called()


@pytest.mark.parametrize(
    'sut_kwargs',
    [
        {
            'cocoapods': True,
            'prepare_simulator': False,
            'version': '0.0.2',
            'build_number': 2,
        }
    ],
)
def test_pre_run_with_params(sut: BaseIOSMixin, bag):
    sut.pre_run()
    bag.pod_install.assert_called()
    bag.prepare_simulator.assert_not_called()
    bag.bump_version.assert_called_with(to_value='0.0.2')
    bag.bump_build_number.assert_called_with(to_value=2)
