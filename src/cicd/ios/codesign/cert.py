import typing as t

from cicd.core.logger import logger
from cicd.core.typing import StrPath


class Certificate:
    def __init__(self, path: StrPath, password: t.Optional[str] = None) -> None:
        self.path = path
        self.password = password or ''

    def install(self, keychain, whitelisted_apps):
        logger.debug(f'Install certificate: {self.path}')
        keychain.import_cert(
            path=self.path,
            password=self.password,
            whitelisted_apps=whitelisted_apps,
        )
