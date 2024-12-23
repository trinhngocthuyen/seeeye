import logging
import os
import sys

try:
    import colorlog

    _has_colorlog = True
except:
    _has_colorlog = False


def default_formatter(fmt=None):
    fmt = fmt or '[%(asctime)s] [%(levelname)s] %(message)s'
    datefmt = '%H:%M:%S'
    # Enable colorlog if you run from terminal or on CI environment
    if _has_colorlog and (os.isatty(2) or os.environ.get('CI')):
        cformat = '%(log_color)s' + fmt
        colors = {
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
        return colorlog.ColoredFormatter(cformat, datefmt, log_colors=colors)
    else:
        return logging.Formatter(fmt, datefmt)


def setup_logger(name, fmt=None) -> logging.Logger:
    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = default_formatter(fmt=fmt)
    handler.setFormatter(formatter)
    this = logging.getLogger(name=name)
    this.setLevel(logging.DEBUG)
    this.addHandler(handler)
    return this


logger = setup_logger(__name__)
