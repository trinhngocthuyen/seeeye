from unittest import mock

import pytest


@pytest.fixture
def mock_derived_data_path_for_action(mock_derived_data_path):
    with mock.patch(
        'cicd.ios.actions.xcodebuild.test.XCBTestAction.derived_data_path',
        new_callable=mock.MagicMock(return_value=mock_derived_data_path),
    ):
        yield mock_derived_data_path


@pytest.fixture
def mock_super_run(bag):
    with mock.patch('cicd.ios.actions.xcodebuild.base.XCBAction.run', bag.super_run):
        yield
