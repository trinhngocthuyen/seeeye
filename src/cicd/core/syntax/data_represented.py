from pathlib import Path
from typing import Any, Dict, List, NewType, Union


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
