import click

from cicd.ios._cli.opts import Opts
from cicd.ios.mixin.mono import MonoMixin as Mixin

opts = Opts(
    workspace=click.option('--workspace', type=str, help='Path to the xcworkspace'),
    scheme=click.option('--scheme', type=str, help='Scheme'),
    project=click.option('--project', type=str, help='Path to the xcodeproj'),
    target=click.option('--target', type=str, help='Target'),
    derived_data_path=click.option(
        '--derived-data-path', type=str, help='DerivedData directory'
    ),
    configuration=click.option(
        '--configuration', type=str, help='Configuration (ex. Debug, Release)'
    ),
    sdk=click.option('--sdk', type=str, help='SDK (ex. iphonesimulator)'),
    destination=click.option(
        '--destination',
        type=str,
        help='Destination (ex. "platform=iOS Simulator,name=iPhone 8"',
    ),
    clean=click.option('--clean', is_flag=True, help='Perform a clean build'),
    log_formatter=click.option(
        '--log-formatter', type=str, help='Log formatter (ex. xcpretty)'
    ),
    log_path=click.option(
        '--log-path', type=str, help='Path to save the xcodebuild log'
    ),
    xcargs=click.option(
        '--xcargs',
        type=str,
        multiple=True,
        help='Overriden settings (ex. SETTINGS=VALUE)',
    ),
    timeout=click.option(
        '--timeout', type=int, help='Timeout (s) of the xcodebuild task'
    ),
    shards=click.option('--shards', type=int, help='Number of shards'),
    shard_idx=click.option(
        '--shard-idx', type=int, help='The shard idx (starting with 1)'
    ),
)

xcodebuild_opts = opts.use(
    'workspace',
    'scheme',
    'project',
    'target',
    'derived_data_path',
    'configuration',
    'sdk',
    'destination',
    'clean',
    'log_formatter',
    'log_path',
    'xcargs',
    'timeout',
    'shards',
    'shard_idx',
)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--build-for-testing', is_flag=True, help='Build for testing')
@click.option('--cocoapods', is_flag=True, help='Run pod install beforehand')
@xcodebuild_opts
def build(**kwargs):
    Mixin().start_building(**kwargs)


@cli.command()
@click.option('--retries', type=int, help='Number of test retries')
@click.option('--only-testing', multiple=True, help='Run only these tests')
@click.option('--test-without-building', is_flag=True, help='Test without building')
@click.option('--cocoapods', is_flag=True, help='Run pod install beforehand')
@xcodebuild_opts
def test(**kwargs):
    Mixin().start_testing(**kwargs)


@cli.command()
@click.option('--config', help='Path to config file (default: .cov.yml)')
@click.option('--export', help='Path to export cov json data')
@opts.use('timeout', 'derived_data_path')
def cov(**kwargs):
    Mixin().start_parsing_cov(**kwargs)


if __name__ == '__main__':
    cli()
