import pytest

from cicd.core.version import Version


@pytest.mark.parametrize(
    'base, component, expected',
    [
        ('0.0.1', 'major', '1.0.1'),
        ('0.0.1', 'minor', '0.1.1'),
        ('0.0.1', 'micro', '0.0.2'),
    ],
)
def test_version_next(base, component, expected):
    next_version = Version(base).next(component)
    assert isinstance(next_version, Version)
    assert str(next_version) == expected
