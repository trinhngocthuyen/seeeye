import typing as t
from pathlib import Path

from cicd.core.security.keychain import Keychain

from .cert import Certificate
from .profile import ProvisioningProfile


class CodeSign:
    def __init__(self, **kwargs) -> None:
        dir = kwargs.get('dir')
        self.dir = Path(dir).expanduser() if dir else None
        self.keychain = Keychain(
            name=kwargs.get('keychain_name'),
            password=kwargs.get('keychain_password'),
        )
        self.cert_password = kwargs.get('cert_password')
        self.profiles: t.List[ProvisioningProfile] = []
        self.certs: t.List[Certificate] = []

    def resolve_profiles_and_certs(self):
        self.profiles = [
            ProvisioningProfile(p) for p in self.dir.glob('**/*.mobileprovision')
        ]
        self.certs = [
            Certificate(p, self.cert_password) for p in self.dir.glob('**/*.p12')
        ]

    def prepare(self):
        self.resolve_profiles_and_certs()
        self.keychain.prepare()
        for profile in self.profiles:
            profile.install()
        for cert in self.certs:
            cert.install(keychain=self.keychain, whitelisted_apps=['/usr/bin/codesign'])

    def cleanup(self):
        try:
            self.keychain.delete()
        except:
            pass
