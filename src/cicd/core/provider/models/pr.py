from .base import ProviderModel


class PullRequest(ProviderModel):
    __desc__ = ['id', 'title']
    id: int
    title: str
