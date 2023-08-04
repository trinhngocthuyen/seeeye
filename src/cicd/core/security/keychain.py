import typing as t
from pathlib import Path

from cicd.core.logger import logger
from cicd.core.utils.sh import sh


class Keychain:
    def __init__(self, **kwargs) -> None:
        self.name: str = kwargs.get('name') or 'cicd'
        self.password: str = kwargs.get('password') or ''

    def prepare(self):
        logger.info(f'Prepare keychain: {self.name}')
        try:
            self.delete()
        except:
            pass
        self.create()
        self.add_to_user_search_list()
        self.unlock()
        return self

    def __enter__(self):
        return self.prepare()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete()

    def create(self):
        sh.exec(
            f'security create-keychain -p {sh.quote(self.password)} {self.name}',
            masked=self.password,
        )

    def delete(self):
        sh.exec(f'security delete-keychain {self.name}')

    def unlock(self):
        sh.exec(
            f'security unlock-keychain -p {sh.quote(self.password)} {self.name}',
            masked=self.password,
        )

    def user_search_list(self) -> t.List[str]:
        output = sh.exec(f'security list-keychain -d user', capture_output=True)
        return [line.strip().strip('"') for line in output.split('\n')]

    def add_to_user_search_list(self):
        current = self.user_search_list()
        cmd = 'security list-keychain -d user -s {} {}'.format(
            ' '.join(sh.quote(x) for x in current), self.name
        )
        sh.exec(cmd)

    def import_cert(
        self,
        path: t.Union[str, Path],
        password: t.Union[str, None] = None,
        whitelisted_apps: t.Optional[t.List[str]] = None,
    ):
        cmd = 'security import {} -P {} -k {}'.format(
            sh.quote(path),
            sh.quote(password or ''),
            self.name,
        )
        for app in whitelisted_apps or []:
            cmd += f' -T {sh.quote(app)}'
        sh.exec(cmd, masked=self.password)
