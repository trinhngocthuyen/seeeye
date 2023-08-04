import base64
import typing as t
from enum import Enum
from pathlib import Path

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from cicd.core.logger import logger
from cicd.core.typing import StrPath


class Cipher:
    class Action(Enum):
        ENCRYPTION = 'enc'
        DECRYPTION = 'dec'

        @property
        def verb(self) -> str:
            return {
                self.ENCRYPTION: 'encrypt',
                self.DECRYPTION: 'decrypt',
            }.get(self)

    def __init__(self, password: str) -> None:
        self.password = password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'',
            iterations=1,
        )
        self.key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.fernet = Fernet(self.key)

    def _perform(
        self,
        action: Action,
        input: t.Union[bytes, str],
    ) -> bytes:
        fn = {
            Cipher.Action.ENCRYPTION: self.fernet.encrypt,
            Cipher.Action.DECRYPTION: self.fernet.decrypt,
        }.get(action)
        return fn(input)

    def perform(
        self,
        action: Action,
        in_path: StrPath,
        out_path: t.Optional[StrPath] = None,
    ):
        def transform_suffix(suffix: str) -> str:
            if action == Cipher.Action.ENCRYPTION:
                return f'{suffix}.enc'
            if action == Cipher.Action.DECRYPTION and suffix == '.enc':
                return ''
            return suffix

        in_path = Path(in_path)
        if out_path:
            out_path = Path(out_path)
        else:
            out_path = in_path.with_suffix(f'.{action.value}')
        logger.info(f'{action.verb.capitalize()}: {in_path} -> {out_path}')

        in_paths, out_paths = [], []
        if in_path.is_dir():
            in_paths = [
                p
                for p in in_path.glob('**/*')
                if not p.is_dir() and not p.stem.startswith('.')
            ]
            out_paths = [
                out_path
                / (p.relative_to(in_path)).with_suffix(transform_suffix(p.suffix))
                for p in in_paths
            ]
        else:
            in_paths = [in_path]
            out_paths = [out_path]

        for (in_file, out_file) in zip(in_paths, out_paths):
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_bytes(
                self._perform(action=action, input=in_file.read_bytes())
            )
