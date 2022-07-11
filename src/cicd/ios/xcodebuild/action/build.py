from .base import XCBAction


class BuildError(Exception):
    pass


class XCBBuildAction(XCBAction):
    def run(self, **kwargs):
        try:
            if not kwargs.get('actions'):
                kwargs['actions'] = ['build']
            return super().run(**kwargs)
        except Exception as e:
            raise BuildError(e)
