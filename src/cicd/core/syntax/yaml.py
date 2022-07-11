import yaml

from .data_represented import DataRepresentedObject


class YAML(DataRepresentedObject):
    def _load_data(self, f):
        return yaml.safe_load(f)

    def _write_data(self, data, f, **kwargs):
        yaml.safe_dump(data, f, **kwargs)
