from cicd.ios.actions.cov import CovAction

from .base_ios import BaseIOSMixin


class CovMixin(BaseIOSMixin):
    def start_parsing_cov(self):
        return CovAction(**self.kwargs).run()
