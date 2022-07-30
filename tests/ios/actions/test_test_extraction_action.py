import pytest

from cicd.core.utils.sh import sh
from cicd.ios.actions.test_extraction import TestExtractionAction


@pytest.fixture
def sut(bag, monkeypatch, mock_metadata_mixin, mock_derived_data_path):
    def mock_exec(*args, **kwargs):
        if args and args[0].startswith('xcrun nm'):
            return '''
0000000000002ae0 T A.B.testC1() -> ()
0000000000002b00 t @objc A.B.testC1() -> ()
0000000000003d60 S method descriptor for A.B.testC1() throws -> ()
0000000000002c60 T A.B.testC2() throws -> ()
0000000000002c80 t @objc A.B.testC2() throws -> ()
0000000000003d68 S method descriptor for A.B.testC2() throws -> ()'''

    bag.metadata.default_derived_data_path = mock_derived_data_path
    (bag.derived_data_path / 'dummy.xctest').mkdir(parents=True)
    monkeypatch.setattr(sh, 'exec', mock_exec)
    return TestExtractionAction()


def test_test_extraction(sut: TestExtractionAction, bag):
    assert sut.run() == ['A/B/testC1', 'A/B/testC2']
