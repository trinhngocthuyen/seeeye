import click

from cicd.core._cli.opts import Opts
from cicd.ios.codesign.cli import main as codesign
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
        help='Destination (ex. "platform=iOS Simulator,name=Seeeye"',
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
    version=click.option('--version', type=str, help='Bump version to this one'),
    version_next=click.option(
        '--version-next', is_flag=True, help='Bump version to the next one'
    ),
    build_number=click.option(
        '--build-number', type=int, help='Bump build number to this one'
    ),
    build_number_next=click.option(
        '--build-number-next', is_flag=True, help='Bump build number to the next one'
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

version_opts = opts.use(
    'version',
    'version_next',
    'build_number',
    'build_number_next',
)


@click.group()
def main():
    pass


@main.command()
@click.option('--build-for-testing', is_flag=True, help='Build for testing')
@click.option('--cocoapods', is_flag=True, help='Run pod install beforehand')
@xcodebuild_opts
@version_opts
def build(**kwargs):
    Mixin(**kwargs).start_building()


@main.command()
@click.option('--retries', type=int, help='Number of test retries')
@click.option('--only-testing', multiple=True, help='Run only these tests')
@click.option('--test-without-building', is_flag=True, help='Test without building')
@click.option('--cocoapods', is_flag=True, help='Run pod install beforehand')
@click.option(
    '--parallel-testing-workers', type=int, help='Number of parallel testing workers'
)
@xcodebuild_opts
@version_opts
def test(**kwargs):
    Mixin(**kwargs).start_testing()


@main.command()
@click.option(
    '--profiles',
    help='Profiles mapping used for exporting to .ipa (format: <bundle_id>:<profile_name>)',
)
@click.option('--export-method', help='Export method (Ex: app-store, ad-hoc...)')
@click.option('--output-path', help='Where the ipa should be in')
@click.option('--archive-path', help='Archive path')
@click.option('--cocoapods', is_flag=True, help='Run pod install beforehand')
@xcodebuild_opts
@version_opts
def archive(**kwargs):
    Mixin(**kwargs).start_archiving()


@main.command()
@click.option('--config', help='Path to config file (default: .cov.yml)')
@click.option('--export', help='Path to export cov json data')
@opts.use('timeout', 'derived_data_path')
def cov(**kwargs):
    Mixin(**kwargs).start_parsing_cov()


@main.command
@version_opts
def bump(**kwargs):
    Mixin().bump(**kwargs)


main.add_command(codesign, name='codesign')


if __name__ == '__main__':
    main()
