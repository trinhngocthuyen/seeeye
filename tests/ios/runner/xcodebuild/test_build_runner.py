import pytest

from cicd.ios.runner.xcodebuild.build import XCBBuildAction, XCBBuildRunner


@pytest.fixture
def sut():
    return XCBBuildRunner()


def test_build_runner_action_cls(sut: XCBBuildRunner):
    assert sut.action_cls == XCBBuildAction
