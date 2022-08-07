from cicd.ios.cov import Cov, CovReport

from .base import IOSAction


class CovAction(IOSAction):
    report: CovReport

    def run(self):
        with self.collect_xcresults(new_only=False):
            pass
        cov = Cov(
            xcresult_path=self.xcresult.path,
            config_path=self.kwargs.get('config'),
        )
        self.report = cov.report
        self.logger.info(
            'Total coverage: {:.1f}%'.format(self.report.total_coverage * 100)
        )
        path_to_export = self.kwargs.get('export')
        if path_to_export:
            self.logger.info(f'Export coverage data to: {path_to_export}')
            self.report.export(path=path_to_export)
