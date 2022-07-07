import re
from pathlib import Path
from typing import Any, Dict, List, Union


class DataRepresentedObject:
    def __init__(
        self,
        data: Union[Dict[str, Any], List[Dict[str, Any]], None] = None,
        path: Union[str, Path, None] = None,
    ) -> None:
        self.data: Union[Dict[str, Any], List[Dict[str, Any]]] = data
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

    def save(self, path: Union[str, Path, None] = None, **kwargs):
        with open(path or self.path, 'w') as f:
            self._write_data(self.data, f, **kwargs)

    def query(self, key: str) -> Union[Dict[str, Any], List[Dict[str, Any]], None]:
        def str_or_int(s: str) -> Union[str, int]:
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
                return None
        return cur
