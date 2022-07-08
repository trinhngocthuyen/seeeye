import json

from .data_represented import DataRepresentedObject


class JSON(DataRepresentedObject):
    def _load_data(self, f):
        return json.load(f)

    def _write_data(self, data, f, **kwargs):
        json.dump(data, f, **kwargs)

    def to_str(self, **kwargs) -> str:
        return json.dumps(self.data, **kwargs)

    @staticmethod
    def from_str(s: str) -> 'JSON':
        return JSON(data=json.loads(s))
