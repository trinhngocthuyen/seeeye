import typing as t
from pathlib import Path

from cicd.core.cipher.cipher import Cipher
from cicd.core.security.keychain import Keychain

from .cert import Certificate
from .profile import ProvisioningProfile


class CodeSign:
    def __init__(self, **kwargs) -> None:
        self.cipher = None
        self.enc_dir = None
        self.dir = None

        if (cipher_password := kwargs.get('password')) is not None:
            self.cipher = Cipher(password=cipher_password)
        if (enc_dir := kwargs.get('enc_dir')) is not None:
            self.enc_dir = enc_dir
        if (dir := kwargs.get('dir')) is not None:
            self.dir = Path(dir).expanduser()
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

    def decrypt_cipher_if_needed(self):
        if not self.cipher:
            return

        self.cipher.perform(
            action=Cipher.Action.DECRYPTION,
            in_path=self.enc_dir,
            out_path=self.dir,
        )

    def prepare(self):
        self.decrypt_cipher_if_needed()
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
