from cicd.core.logger import logger


class BuildJob:
    def run(self):
        logger.warning(f'To be implemented <{self.__class__.__name__}>')


if __name__ == '__main__':
    BuildJob().run()
