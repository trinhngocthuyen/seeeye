import pytest

from cicd.core.syntax.json import JSON


@pytest.fixture
def json_path(tmp_path):
    return tmp_path / 'dummy.json'


def test_json_load(json_path):
    json_path.write_text('{"one": 1, "two": 2}')
    json_data = JSON(path=json_path)
    assert json_data.data == {'one': 1, 'two': 2}
    assert json_data.to_str() == '{"one": 1, "two": 2}'


def test_json_write(json_path):
    json_data = JSON(path=json_path)
    json_data.data = {'one': 1}
    json_data.save()
    assert json_path.read_text() == '{"one": 1}'
