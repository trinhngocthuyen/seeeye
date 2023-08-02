from unittest import mock

import pytest

from cicd.ios.codesign.codesign import CodeSign


@pytest.fixture
def codesign_dir(tmp_path):
    (tmp_path / 'cert.p12').touch()
    (tmp_path / 'profile.mobileprovision').touch()
    return tmp_path


@pytest.fixture
def sut(codesign_dir, bag, monkeypatch):
    with mock.patch('cicd.core.utils.file.FileUtils.copy', new=bag.fileutils.copy):
        this = CodeSign(dir=codesign_dir)
        monkeypatch.setattr(this, 'keychain', bag.keychain)
        yield this


def test_codesign_prepare(sut: CodeSign, bag):
    sut.prepare()
    assert len(sut.profiles) == 1
    assert len(sut.certs) == 1
    bag.keychain.prepare.assert_called()
    bag.keychain.import_cert.assert_called()
    bag.fileutils.copy.assert_called()


def test_codesign_cleanup(sut: CodeSign, bag):
    sut.cleanup()
    bag.keychain.delete.assert_called()
