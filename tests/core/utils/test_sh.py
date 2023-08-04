import pytest

from cicd.core.utils.sh import Shell, sh


def test_sh_exec_masking(caplog):
    sh.exec('echo my password is: abcxyz', masked='abcxyz', log_cmd=True)
    assert 'my password is' in caplog.text
    assert 'abcxyz' not in caplog.text


def test_sh_exec_masking_when_failed(caplog):
    with pytest.raises(
        Shell.ExecError, match=r'my password is: \*\*\*\*\*masked\*\*\*\*\*'
    ):
        sh.exec('echo my password is: abcxyz && exit 65', masked='abcxyz', log_cmd=True)
    assert 'abcxyz' not in caplog.text
