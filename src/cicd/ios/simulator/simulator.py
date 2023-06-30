import re
import shlex
import typing as t
from contextlib import contextmanager
from functools import cached_property

from cicd.core.logger import logger
from cicd.core.syntax.json import JSON
from cicd.core.utils.sh import sh

__all__ = ['Simulator']


class SimCtlMixin:
    def simctl(self, *args, **kwargs):
        return sh.exec('xcrun simctl {}'.format(' '.join(args)), **kwargs)


class Runtime(dict):
    @property
    def name(self) -> str:
        return self.get('name')

    @property
    def version(self) -> str:
        return self.get('version')

    @property
    def identifier(self) -> str:
        return self.get('identifier')

    @property
    def available(self) -> bool:
        return self.get('isAvailable')


class DeviceType(dict):
    @property
    def name(self) -> str:
        return self.get('name')

    @property
    def identifier(self) -> str:
        return self.get('identifier')


class Simulator(dict, SimCtlMixin):
    _runtimes: t.List[Runtime]
    _device_types: t.List[DeviceType]
    _devices: t.List['Simulator']

    def __init__(self, **kwargs):
        def dashify(s: str) -> str:
            return re.sub(r'[ \.]', '-', s)

        device_type_name = kwargs.pop('type', None)
        runtime_name = kwargs.pop('runtime', None)
        if 'name' not in kwargs:
            kwargs['name'] = 'Seeeye'
        if device_type_name:
            kwargs[
                'deviceTypeIdentifier'
            ] = 'com.apple.CoreSimulator.SimDeviceType.{}'.format(
                dashify(device_type_name)
            )
        if runtime_name:
            if not runtime_name.startswith('iOS'):
                runtime_name = f'iOS {runtime_name}'
            kwargs[
                'runtimeIdentifier'
            ] = 'com.apple.CoreSimulator.SimRuntime.{}'.format(dashify(runtime_name))
        super().__init__(**kwargs)

    def __str__(self) -> str:
        return '{} ({}) ({}, {})'.format(
            self.name, self.identifier, self.device_type.name, self.run_time.name
        )

    @property
    def identifier(self) -> str:
        return self.get('udid')

    @property
    def name(self) -> str:
        return self.get('name')

    @property
    def state(self) -> str:
        return self.get('state')

    @property
    def log_path(self) -> str:
        return self.get('logPath')

    @property
    def data_path(self) -> str:
        return self.get('dataPath')

    @property
    def available(self) -> bool:
        return self.get('isAvailable')

    @cached_property
    def run_time(self) -> Runtime:
        runtime_id = self.get('runtimeIdentifier')
        if runtime_id:
            predicate = lambda x: x.identifier == runtime_id
        else:
            predicate = lambda x: x.name.startswith('iOS')
        return next(x for x in self._runtimes if predicate(x))

    @cached_property
    def device_type(self) -> DeviceType:
        device_type_id = self.get('deviceTypeIdentifier')
        if device_type_id:
            predicate = lambda x: x.identifier == device_type_id
        else:
            predicate = lambda x: x.name.startswith('iPhone 14')
        return next(x for x in self._device_types if predicate(x))

    @staticmethod
    def load():
        data = JSON.from_str(sh.exec('xcrun simctl list --json'))
        Simulator._runtimes = [Runtime(x) for x in data['runtimes']]
        Simulator._device_types = [DeviceType(x) for x in data['devicetypes']]
        Simulator._devices = [
            Simulator(runtime_id=runtime_id, **device_data)
            for (runtime_id, devices_data) in data['devices'].items()
            for device_data in devices_data
        ]

    def _find_simulator(self):
        return next((x for x in Simulator._devices if x.name == self.name), None)

    @contextmanager
    def _sync(self):
        Simulator.load()
        existing = self._find_simulator()
        if existing:
            self.update(existing)
        yield

    def create(self):
        logger.info(
            f'Create simulator: {self.name} ({self.device_type.name}, {self.run_time.name})'
        )
        self.simctl(
            'create',
            shlex.quote(self.name),
            self.device_type.identifier,
            self.run_time.identifier,
        )
        with self._sync():
            return self

    def delete(self):
        self.simctl('delete', shlex.quote(self.name or self.identifier))

    def prepare(self) -> 'Simulator':
        with self._sync():
            if self._find_simulator():
                return self
        return self.create()

    def __enter__(self):
        simulator = self.prepare()
        logger.info(f'Simulator: {simulator}')
        return simulator

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def from_xcodebuild_destination(destination: str) -> t.Optional['Simulator']:
        params = dict(tuple(cmp.split('=')) for cmp in destination.split(','))
        if params.get('platform') == 'iOS Simulator':
            return Simulator(
                name=params.get('name'),
                udid=params.get('id'),
                runtime=params.get('OS'),
            )
