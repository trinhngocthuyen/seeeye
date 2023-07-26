from .base import XCBAction


class BuildError(Exception):
    pass


class XCBBuildAction(XCBAction):
    '''A class that interacts with the xcodebuild command, particularly for build actions.'''

    def run(self):
        kwargs = self.kwargs
        try:
            if not kwargs.get('actions'):
                if kwargs.get('build_for_testing'):
                    kwargs['actions'] = ['build-for-testing']
                else:
                    kwargs['actions'] = ['build']
            return super().run()
        except Exception as e:
            raise BuildError(e)
