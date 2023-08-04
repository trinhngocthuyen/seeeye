from unittest import mock

import pytest

from cicd.ios.codesign.codesign import CodeSign


@pytest.fixture
def codesign_dir(tmp_path):
    (tmp_path / 'dec').mkdir(parents=True, exist_ok=True)
    (tmp_path / 'dec' / 'cert.p12').touch()
    (tmp_path / 'dec' / 'profile.mobileprovision').touch()
    return tmp_path


@pytest.fixture
def codesign_enc_dir(tmp_path):
    (tmp_path / 'enc').mkdir(parents=True, exist_ok=True)
    (tmp_path / 'enc' / 'cert.p12.enc').touch()
    (tmp_path / 'enc' / 'profile.mobileprovision.enc').touch()
    return tmp_path


@pytest.fixture
def codesign_password():
    return 'foo'


@pytest.fixture
def codesign_kwargs(codesign_dir, codesign_enc_dir, codesign_password):
    return dict(
        dir=codesign_dir,
        enc_dir=codesign_enc_dir,
        password=codesign_password,
    )


@pytest.fixture
def sut(bag, monkeypatch, codesign_kwargs):
    with mock.patch('cicd.core.utils.file.FileUtils.copy', new=bag.fileutils.copy):
        this = CodeSign(**codesign_kwargs)
        monkeypatch.setattr(this, 'keychain', bag.keychain)
        with mock.patch('cicd.core.cipher.cipher.Cipher.perform', bag.cipher.perform):
            yield this
