from cicd.core.utils.sh import sh

from .metadata import MetadataMixin


class CocoaPodsMixin(MetadataMixin):
    def pod(self, cmd: str):
        sh.exec(
            '{} {}'.format(self.metadata.resolve_program('pod'), cmd),
            capture_output=False,
            log_cmd=True,
        )

    def pod_install(self):
        self.pod('install')

    def prepare_cocoapods(self, **kwargs):
        if kwargs.get('cocoapods'):
            self.pod_install()
