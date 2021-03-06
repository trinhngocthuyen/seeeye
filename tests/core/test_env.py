import pytest

from cicd.core.env import Env


@pytest.mark.parametrize(
    'envname, expected_klazz_name',
    [
        ('GITLAB_CI', 'GitlabEnv'),
        ('GITHUB_ACTIONS', 'GithubEnv'),
    ],
)
def test_env_by_provider(monkeypatch, envname, expected_klazz_name):
    monkeypatch.setenv(envname, 'true')
    Env.reset_provider()
    env = Env().provider
    assert Env.provider_cls().__name__ == expected_klazz_name
    assert env.__class__.__name__ == expected_klazz_name
