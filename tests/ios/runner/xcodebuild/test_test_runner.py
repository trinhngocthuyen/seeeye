import pytest

from cicd.ios.runner.xcodebuild.test import XCBTestAction, XCBTestRunner


@pytest.fixture
def sut():
    return XCBTestRunner()


def test_build_runner_action_cls(sut: XCBTestRunner):
    assert sut.action_cls == XCBTestAction
