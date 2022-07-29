import click

from cicd.ios.actions.xcodebuild.cli import xcodebuild_opts
from cicd.ios.mixin.test import TestMixin


class TestJob(TestMixin):
    def run(self, **kwargs):
        self.start_testing(**kwargs)


@click.command()
@click.option('--retries', type=int, help='Number of test retries')
@click.option('--only-testing', multiple=True, help='Run only these tests')
@click.option('--test-without-building', is_flag=True, help='Test without building')
@click.option('--cocoapods', is_flag=True, help='Run pod install beforehand')
@xcodebuild_opts
def cli(**kwargs):
    TestJob().run(**kwargs)


if __name__ == '__main__':
    cli()
