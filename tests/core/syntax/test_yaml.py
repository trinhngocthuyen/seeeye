import pytest

from cicd.core.syntax.yaml import YAML


@pytest.fixture
def yaml_path(tmp_path):
    return tmp_path / 'dummy.yaml'


def test_yaml_load(yaml_path):
    yaml_path.write_text('{"one": 1, "two": 2}')
    yaml_data = YAML(path=yaml_path)
    assert yaml_data.data == {'one': 1, 'two': 2}


def test_yaml_write(yaml_path):
    yaml_data = YAML(path=yaml_path)
    yaml_data.data = {'one': 1, 'two': 2}
    yaml_data.save()
    assert (
        yaml_path.read_text()
        == '''\
one: 1
two: 2
'''
    )
