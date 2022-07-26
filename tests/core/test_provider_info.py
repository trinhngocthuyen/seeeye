import pytest

from cicd.core.provider.info import ProviderInfo


@pytest.mark.parametrize(
    'envname, expected_provider_name',
    [
        ('GITLAB_CI', 'gitlab'),
        ('GITHUB_ACTIONS', 'github'),
    ],
)
def test_provider_info(monkeypatch, envname, expected_provider_name):
    monkeypatch.setenv(envname, 'true')
    provider_info = ProviderInfo.resolve()
    assert provider_info.name == expected_provider_name
