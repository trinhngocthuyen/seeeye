from pathlib import Path

import pytest

from cicd.ios.xcodebuild.action.test import TestError, XCBTestAction


@pytest.fixture
def sut(bag, mock_derived_data_path_for_action: Path, mock_super_run):
    bag.xcresult_before = (
        mock_derived_data_path_for_action / 'Logs/Test/before.xcresult'
    )
    bag.xcresult_after = mock_derived_data_path_for_action / 'Logs/Test/after.xcresult'
    bag.xcresult_before.mkdir(parents=True)
    return XCBTestAction()


def test_xcb_test_action_success(sut: XCBTestAction, bag):
    bag.super_run.side_effect = lambda: bag.xcresult_after.mkdir(parents=True)
    assert sut.run().path == bag.xcresult_after
    assert sut.xcresult.path == bag.xcresult_after
    bag.super_run.assert_called()


def test_xcb_test_action_failure(sut: XCBTestAction, bag):
    def mock_run():
        bag.xcresult_after.mkdir(parents=True)
        raise RuntimeError('Fail on purpose')

    bag.super_run.side_effect = mock_run
    with pytest.raises(TestError) as excinfo:
        assert sut.run().path == bag.xcresult_after
        assert sut.xcresult.path == bag.xcresult_after
        assert sut.xcresult == excinfo.value.xcresult
        bag.super_run.assert_called()
