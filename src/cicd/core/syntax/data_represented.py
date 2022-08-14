import re
import typing as t
from pathlib import Path

T = t.TypeVar('T', bound='DataRepresentedObject')


class DataRepresentedObject:
    def __init__(
        self,
        data: t.Union[t.Dict[str, t.Any], t.List[t.Dict[str, t.Any]], None] = None,
        path: t.Union[str, Path, None] = None,
    ) -> None:
        self.data: t.Union[t.Dict[str, t.Any], t.List[t.Dict[str, t.Any]]] = data
        self.path = path
        if data is None and path:
            try:
                with open(path) as f:
                    self.data = self._load_data(f)
            except FileNotFoundError:
                self.data = {}

    def _load_data(self, f):
        raise NotImplementedError

    def _write_data(self, data, f):
        raise NotImplementedError

    def save(self, path: t.Union[str, Path, None] = None, **kwargs):
        p = Path(path or self.path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, 'w') as f:
            self._write_data(self.data, f, **kwargs)

    def as_type(self, t: t.Type[T]) -> T:
        return t(data=self.data, path=self.path)

    def query(
        self,
        key: str,
        as_type: t.Optional[t.Type[T]] = None,
    ) -> t.Union[T, t.Dict[str, t.Any], t.List[t.Dict[str, t.Any]], None]:
        def str_or_int(s: str) -> t.Union[str, int]:
            try:
                return int(s)
            except ValueError:
                return s

        key_cmps = [str_or_int(x) for x in re.split(r'\.|\[', key.replace(']', ''))]
        cur = self.data
        for cmp in key_cmps:
            if isinstance(cmp, str) and isinstance(cur, dict) and cmp in cur:
                cur = cur.get(cmp)
            elif isinstance(cmp, int) and isinstance(cur, list) and len(cur) > cmp:
                cur = cur[cmp]
            else:
                cur = None
                break
        return as_type(data=cur, path=self.path) if as_type else cur
