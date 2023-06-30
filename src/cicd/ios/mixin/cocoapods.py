from functools import cached_property

from cicd.core.utils.sh import sh

from .metadata import MetadataMixin


class CocoaPodsMixin(MetadataMixin):
    @cached_property
    def pod_bin(self):
        return self.metadata.resolve_program('pod')

    def pod(self, cmd: str):
        sh.exec(
            f'{self.pod_bin} {cmd}',
            capture_output=False,
            log_cmd=True,
        )

    def pod_install(self):
        self.pod('install')

    def prepare_cocoapods(self, **kwargs):
        if kwargs.get('cocoapods'):
            self.pod_install()
