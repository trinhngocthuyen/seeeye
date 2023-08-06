from unittest import mock

import pytest


@pytest.fixture
def mock_pre_run_and_post_run(bag):
    with mock.patch('cicd.ios.mixin.base_ios.BaseIOSMixin.pre_run', bag.pre_run):
        with mock.patch('cicd.ios.mixin.base_ios.BaseIOSMixin.post_run', bag.post_run):
            with mock.patch('cicd.ios.runner.base.Runner.run', bag.runner.run):
                yield
