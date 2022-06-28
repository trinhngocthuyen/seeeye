import os

from cicd.core.mixin.provider import ProviderMixin


class Env(ProviderMixin):
    ci: bool = os.getenv('CI') == 'true'
