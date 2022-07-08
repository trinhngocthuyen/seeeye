from functools import cached_property
from pathlib import Path
from typing import List, Optional, Union

from cicd.core.syntax.json import JSON

from .xcresulttool import XCResultToolMixin


class Metadata(JSON):
    @cached_property
    def tests_ref_id(self) -> str:
        return self.query('actions._values[0].actionResult.testsRef.id._value')

    @cached_property
    def log_ref_id(self) -> str:
        return self.query('actions._values[0].actionResult.logRef.id._value')


class TestItemData(JSON):
    @cached_property
    def uri(self) -> str:
        return self.query('identifierURL._value')

    @cached_property
    def uri_cmps(self) -> List[str]:
        return self.uri.split('/')

    @property
    def fullname(self) -> str:
        return f'{self.target}/{self.suite}/{self.name}'

    @property
    def name(self) -> str:
        return self.uri_cmps[-1]

    @property
    def suite(self) -> str:
        return self.uri_cmps[-2]

    @property
    def target(self) -> str:
        return self.uri_cmps[-3]

    @cached_property
    def status(self) -> str:
        return self.query('testStatus._value')

    @cached_property
    def duration(self) -> float:
        return self.query('duration._value')

    @property
    def is_success(self) -> bool:
        return self.status == 'Success'


class TestsData(JSON):
    @cached_property
    def summaries(self) -> List[TestItemData]:
        def to_jsons(xs: list) -> List[JSON]:
            return [JSON(data=x) for x in xs]

        result = []
        to_traverse = to_jsons(
            self.query('summaries._values[0].testableSummaries._values')
        )
        while to_traverse:
            item = to_traverse.pop(0)
            to_traverse += to_jsons(item.query('tests._values') or [])
            to_traverse += to_jsons(item.query('subtests._values') or [])
            if 'testStatus' in item.data:
                result.append(item.as_type(TestItemData))
        return result


class XCResult(XCResultToolMixin):
    def __init__(
        self,
        path: Optional[Union[str, Path]] = None,
    ) -> None:
        self.path = path

    def extract_raw(self, id) -> JSON:
        return self.xcresulttool.get(path=self.path, id=id, to_json=True)

    @cached_property
    def metadata(self) -> Metadata:
        return self.extract_raw(id=None).as_type(Metadata)

    @cached_property
    def tests_data(self) -> TestsData:
        return self.extract_raw(id=self.metadata.tests_ref_id).as_type(TestsData)

    @property
    def test_summaries(self) -> List[TestItemData]:
        return self.tests_data.summaries

    @property
    def tests(self) -> List[str]:
        return [x.fullname for x in self.test_summaries]

    @property
    def failed_tests(self) -> List[str]:
        return [x.fullname for x in self.test_summaries if not x.is_success]
