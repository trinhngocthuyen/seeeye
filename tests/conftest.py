from unittest import mock

import pytest


@pytest.fixture
def bag():
    return mock.MagicMock()
