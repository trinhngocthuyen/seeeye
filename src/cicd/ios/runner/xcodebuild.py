from functools import cached_property

from cicd.ios.xcodebuild.action import XCBAction, XCBBuildAction, XCBTestAction

from .base import BuildRunner, Runner, TestRunner


class XCBRunner(Runner):
    def run(self, **kwargs):
        return self.action.run(**kwargs)

    @cached_property
    def action(self):
        return XCBAction()


class XCBBuildRunner(XCBRunner, BuildRunner):
    @cached_property
    def action(self):
        return XCBBuildAction()


class XCBTestRunner(XCBRunner, TestRunner):
    @cached_property
    def action(self):
        return XCBTestAction()
