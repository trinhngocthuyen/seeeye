from functools import cached_property

from git.repo import Repo


class GitMixin:
    @cached_property
    def repo(self) -> Repo:
        return Repo()

    @property
    def git(self):
        return self.repo.git
