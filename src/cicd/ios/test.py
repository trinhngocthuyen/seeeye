import click

from cicd.ios.mixin.test import TestMixin
from cicd.ios.xcodebuild.cli import xcodebuild_opts


class TestJob(TestMixin):
    def run(self, **kwargs):
        self.start_testing(**kwargs)


@click.command()
@click.option('--test-without-building', is_flag=True, help='Test without building')
@xcodebuild_opts
def cli(**kwargs):
    TestJob().run(**kwargs)


if __name__ == '__main__':
    cli()
