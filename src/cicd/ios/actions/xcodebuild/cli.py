import functools

import click


def xcodebuild_opts(func):
    @click.option('--shard-idx', type=int, help='The shard idx (starting with 1)')
    @click.option('--shards', type=int, help='Number of shards')
    @click.option('--timeout', type=int, help='Timeout (s) of the xcodebuild task')
    @click.option(
        '--xcargs',
        type=str,
        multiple=True,
        help='Overriden settings (ex. SETTINGS=VALUE)',
    )
    @click.option('--log-path', type=str, help='Path to save the xcodebuild log')
    @click.option('--log-formatter', type=str, help='Log formatter (ex. xcpretty)')
    @click.option('--clean', is_flag=True, help='Perform a clean build')
    @click.option(
        '--destination',
        type=str,
        help='Destination (ex. "platform=iOS Simulator,name=iPhone 8"',
    )
    @click.option('--sdk', type=str, help='SDK (ex. iphonesimulator)')
    @click.option(
        '--configuration', type=str, help='Configuration (ex. Debug, Release)'
    )
    @click.option('--derived-data-path', type=str, help='DerivedData directory')
    @click.option('--target', type=str, help='Target')
    @click.option('--project', type=str, help='Path to the xcodeproj')
    @click.option('--scheme', type=str, help='Scheme')
    @click.option('--workspace', type=str, help='Path to the xcworkspace')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)

    return wrapper
