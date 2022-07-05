import click

from cicd.ios.mixin.build import BuildMixin
from cicd.ios.xcodebuild.cli import xcodebuild_opts


class BuildJob(BuildMixin):
    def run(self, **kwargs):
        self.start_building(**kwargs)


@click.command()
@xcodebuild_opts
def cli(**kwargs):
    BuildJob().run(**kwargs)


if __name__ == '__main__':
    cli()
