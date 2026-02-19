import logging
from datetime import datetime
from logging.config import dictConfig
from pathlib import Path
from typing import Literal

LOG_FILENAME_PREFIX = 'log'
LOG_FILENAME_EXT = 'txt'
LOG_FILENAME_TIMESTAMP_FORMAT = '%Y%m%d-%H%M%S'
DEFAULT_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '\n\n[%(asctime)s] %(levelname)-8s @ %(filename)s:%(lineno)d\n%(message)s',
            'datefmt': '%d-%m-%Y:%H:%M:%S'
        }
    }
}


def generate_log_filename() -> str:
    timestamp = datetime.now().strftime(LOG_FILENAME_TIMESTAMP_FORMAT)
    filename = f'{LOG_FILENAME_PREFIX}-{timestamp}.{LOG_FILENAME_EXT}'
    return filename


def create_logger(
    *,
    name: str,
    level: Literal['WARNING', 'DEBUG'],
    log_file: Path
) -> logging.Logger:
    # config
    config = dict(**DEFAULT_CONFIG, **{
        'handlers': {
            name: {
                'class': 'logging.FileHandler',
                'level': level,
                'formatter': 'standard',
                'filename': log_file,
                'mode': 'w',
                'delay': True
            }
        },
        'loggers': {
            name: {
                'level': level,
                'handlers': [name, ],
                'propagate': False
            }
        }
    })
    # logger
    dictConfig(config)
    logger = logging.getLogger(name)

    # return
    return logger
