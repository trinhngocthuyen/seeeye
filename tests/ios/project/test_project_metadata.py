from pathlib import Path

import pytest

from cicd.ios.project.metadata import Metadata


@pytest.fixture
def schemes():
    return ['EX']


@pytest.fixture
def sut(tmp_path, schemes):
    (tmp_path / 'EX.xcworkspace').mkdir()
    (tmp_path / 'EX.xcodeproj').mkdir()
    for scheme in schemes:
        scheme_path = (
            tmp_path
            / 'EX.xcodeproj'
            / 'xcshareddata'
            / 'xcschemes'
            / f'{scheme}.xcscheme'
        )
        scheme_path.parent.mkdir(parents=True, exist_ok=True)
        scheme_path.touch()
    return Metadata()


def test_project_metadata_mixin(sut: Metadata):
    assert sut.project_name == 'EX'
    assert sut.schemes == ['EX']
    assert sut.scheme == 'EX'
    assert sut.workdir == Path()
    assert sut.xcodeproj_path == Path('EX.xcodeproj')
    assert sut.pbxproj_path == Path('EX.xcodeproj/project.pbxproj')
    assert sut.xcworkspace_path == Path('EX.xcworkspace')


@pytest.mark.parametrize('schemes', [[]])
def test_no_scheme_warning(sut: Metadata, caplog):
    assert sut.schemes == []
    assert sut.scheme is None
    assert 'Detect no shared scheme' in caplog.text


@pytest.mark.parametrize('schemes', [['EX', 'EX2']])
def test_multiple_schemes_warning(sut: Metadata, caplog):
    assert sut.scheme == 'EX'
    assert sut.schemes == ['EX', 'EX2']
    assert 'Detect multiple schemes' in caplog.text
