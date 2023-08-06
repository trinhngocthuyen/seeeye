from unittest import mock

import pytest


@pytest.fixture
def bag():
    return mock.MagicMock()


@pytest.fixture(autouse=True)
def change_workdir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
