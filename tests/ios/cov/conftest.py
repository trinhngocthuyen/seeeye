import pytest

from cicd.ios.cov import CovConfig, CovReport


@pytest.fixture
def cov_config(tmp_path):
    config_path = tmp_path / '.cov.yml'
    config_path.write_text(
        """
targets:
    - A1.app
    - A2.app

path_mapping:
    from: '^\\S+\\/project\\/'
    to: ''

ignore:
    - '*.generated.*'
    - 'src/ignored/*'
"""
    )
    return CovConfig(path=config_path)


@pytest.fixture
def cov_report(cov_config):
    raw = {
        'targets': [
            {
                'name': 'A1.app',
                'files': [
                    {
                        'coveredLines': 1,
                        'executableLines': 2,
                        'path': 'path/to/project/src/A1/X1.swift',
                    },
                    {
                        'coveredLines': 0,
                        'executableLines': 2,
                        'path': 'path/to/project/src/A1/X2.swift',
                    },
                    {
                        'coveredLines': 0,
                        'executableLines': 2,
                        'path': 'path/to/project/src/X3.generated.swift',
                    },
                    {
                        'coveredLines': 0,
                        'executableLines': 2,
                        'path': 'path/to/project/src/ignored/X4.swift',
                    },
                ],
            },
            {
                'name': 'B1.xctest',
                'files': [
                    {
                        'coveredLines': 2,
                        'executableLines': 2,
                        'path': 'path/to/project/tests/B1/X1.swift',
                    }
                ],
            },
        ],
    }
    return CovReport(raw=raw, config=cov_config)
