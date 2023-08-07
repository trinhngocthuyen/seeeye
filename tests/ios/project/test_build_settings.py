import pytest

from cicd.ios.project.build_settings import BuildSettings


@pytest.fixture
def sut():
    return BuildSettings.from_xcodebuild_settings(
        '''
User defaults from command line:
    IDEPackageSupportUseBuiltinSCM = YES

Build settings for action build and target EX:
    PRODUCT_BUNDLE_IDENTIFIER = com.thuyen.EX
    EXPANDED_CODE_SIGN_IDENTITY =
    arch = arm64
'''
    )


def test_build_settings_from_raw(sut):
    assert sut == BuildSettings(
        {
            'PRODUCT_BUNDLE_IDENTIFIER': 'com.thuyen.EX',
            'EXPANDED_CODE_SIGN_IDENTITY': '',
            'arch': 'arm64',
        }
    )
