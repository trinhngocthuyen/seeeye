from pathlib import Path

import pytest

from cicd.ios.actions.xcodebuild.build import BuildError, XCBBuildAction


@pytest.fixture
def sut(bag, mock_derived_data_path_for_action: Path, mock_super_run):
    return XCBBuildAction()


def test_xcb_build_action_success(sut: XCBBuildAction, bag):
    sut.run()
    bag.super_run.assert_called()


def test_xcb_build_action_failure(sut: XCBBuildAction, bag):
    def mock_run():
        raise RuntimeError('Fail on purpose')

    bag.super_run.side_effect = mock_run
    with pytest.raises(BuildError):
        sut.run()
        bag.super_run.assert_called()
