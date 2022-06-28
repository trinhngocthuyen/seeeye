from cicd.core.logger import logger


class LoggingMixin:
    @property
    def logger(self):
        return logger
