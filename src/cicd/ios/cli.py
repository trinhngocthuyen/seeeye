import click

from cicd.ios.actions.xcodebuild.cli import xcodebuild_opts
from cicd.ios.mixin.mono import MonoMixin as Mixin


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
@xcodebuild_opts
def cov(**kwargs):
    Mixin().start_parsing_cov(**kwargs)


if __name__ == '__main__':
    cli()
