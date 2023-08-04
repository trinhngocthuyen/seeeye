import pytest

from cicd.core.cipher.cipher import Cipher
from cicd.ios.codesign.codesign import CodeSign


def assert_prepared_certs_and_profiles(sut, bag):
    assert len(sut.profiles) == 1
    assert len(sut.certs) == 1
    bag.keychain.prepare.assert_called()
    bag.keychain.import_cert.assert_called()
    bag.fileutils.copy.assert_called()


@pytest.mark.parametrize('codesign_enc_dir, codesign_password', [(None, None)])
def test_codesign_prepare_without_decryption(sut: CodeSign, bag):
    assert sut.cipher is None
    sut.prepare()
    assert_prepared_certs_and_profiles(sut, bag)
    bag.cipher.perform.assert_not_called()


def test_codesign_prepare_with_decryption(
    sut: CodeSign, bag, codesign_dir, codesign_enc_dir
):
    sut.prepare()
    assert_prepared_certs_and_profiles(sut, bag)
    bag.cipher.perform.assert_called_with(
        action=Cipher.Action.DECRYPTION,
        in_path=codesign_enc_dir,
        out_path=codesign_dir,
    )


def test_codesign_cleanup(sut: CodeSign, bag):
    sut.cleanup()
    bag.keychain.delete.assert_called()
