import click

from cicd.ios.mixin.test import TestMixin
from cicd.ios.xcodebuild.cli import xcodebuild_opts


class TestJob(TestMixin):
    def run(self, **kwargs):
        self.start_testing(**kwargs)


@click.command()
@xcodebuild_opts
def cli(**kwargs):
    TestJob().run(**kwargs)


if __name__ == '__main__':
    cli()
