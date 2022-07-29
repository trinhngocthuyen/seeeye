import click

from cicd.ios.actions.xcodebuild.cli import xcodebuild_opts
from cicd.ios.mixin.build import BuildMixin


class BuildJob(BuildMixin):
    def run(self, **kwargs):
        self.start_building(**kwargs)


@click.command()
@click.option('--build-for-testing', is_flag=True, help='Build for testing')
@click.option('--cocoapods', is_flag=True, help='Run pod install beforehand')
@xcodebuild_opts
def cli(**kwargs):
    BuildJob().run(**kwargs)


if __name__ == '__main__':
    cli()
