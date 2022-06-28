import logging
import os

try:
    import colorlog

    _has_colorlog = True
except:
    _has_colorlog = False

__all__ = ['logger']


def default_formatter():
    format_str = '[%(asctime)s] [%(levelname)s] %(message)s'
    date_format = '%H:%M:%S'
    # Enable colorlog if you run from terminal or on CI environment
    if _has_colorlog and (os.isatty(2) or os.environ.get('CI')):
        cformat = '%(log_color)s' + format_str
        colors = {
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
        return colorlog.ColoredFormatter(cformat, date_format, log_colors=colors)
    else:
        return logging.Formatter(format_str, date_format)


def setup_logger(name) -> logging.Logger:
    handler = logging.StreamHandler()
    formatter = default_formatter()
    handler.setFormatter(formatter)
    this = logging.getLogger(name=name)
    this.setLevel(logging.DEBUG)
    this.addHandler(handler)
    return this


logger = setup_logger(__name__)
