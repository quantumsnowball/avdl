import logging
from logging.config import dictConfig
from pathlib import Path
from typing import Literal

DEFAULT_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
}


def create_logger(name: str,
                  level: Literal['WARNING', 'DEBUG'],
                  log_file: Path) -> logging.Logger:
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
