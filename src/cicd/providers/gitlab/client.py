from cicd.core.provider.client import ProviderClient


class GitlabClient(ProviderClient):
    BASE_URL = 'https://gitlab.com/api/v4'
