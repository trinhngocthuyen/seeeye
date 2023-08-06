import pytest

from cicd.core.version import Version
from cicd.ios.mixin.version import VersionMixin


def gen_pbxproj_content(version: str, build_number: int) -> str:
    return f"""
PRODUCT_NAME = EX;
MARKETING_VERSION = {version};
CURRENT_PROJECT_VERSION = {build_number};
SWIFT_VERSION = 5.0;
"""


@pytest.fixture
def pbxproj_path(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = tmp_path / 'EX.xcodeproj' / 'project.pbxproj'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(gen_pbxproj_content(version='0.0.1', build_number=1))
    return path


@pytest.fixture
def sut(pbxproj_path):
    return VersionMixin()


def test_version_read(sut: VersionMixin):
    assert sut.version == Version('0.0.1')
    assert sut.build_number == 1


def test_version_bump(sut: VersionMixin, pbxproj_path):
    assert sut.bump_version() == Version('0.0.2')
    assert sut.bump_build_number() == 2
    assert pbxproj_path.read_text() == gen_pbxproj_content(
        version='0.0.2', build_number=2
    )
    assert sut.bump_version('0.0.9') == Version('0.0.9')
    assert sut.bump_build_number(9) == 9
    assert pbxproj_path.read_text() == gen_pbxproj_content(
        version='0.0.9', build_number=9
    )

    sut.bump(version='1.0.0', build_number='100')
    assert sut.version == Version('1.0.0')
    assert sut.build_number == 100
