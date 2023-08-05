from packaging import version

__all__ = ['Version']


class Version(version.Version):
    def next(self, component: str = 'micro') -> 'Version':
        idx = {'major': 0, 'minor': 1, 'micro': 2}.get(component)
        parts = list(self.release)
        parts[idx] += 1
        return Version('.'.join(str(x) for x in parts))
