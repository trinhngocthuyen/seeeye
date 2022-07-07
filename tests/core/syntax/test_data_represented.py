import pytest

from cicd.core.syntax.data_represented import DataRepresentedObject


@pytest.fixture
def obj():
    return DataRepresentedObject(
        data={
            'digits': [
                {'key': 'zero', 'value': 0},
                {'key': 'one', 'value': 1},
                {'key': 'two', 'value': 2},
            ],
        }
    )


def test_data_represented_query(obj: DataRepresentedObject):
    assert obj.query('digits[0].key') == 'zero'
    assert obj.query('digits[0].value') == 0
    assert obj.query('digits[1].key') == 'one'
    assert obj.query('digits[1].value') == 1

    assert obj.query('dummy') is None
    assert obj.query('digits[0].dummy') is None
    assert obj.query('digits[0].value.dummy') is None
    assert obj.query('digits[1000].value') is None
