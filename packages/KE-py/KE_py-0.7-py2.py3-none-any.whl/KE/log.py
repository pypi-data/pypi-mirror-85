import logging
import logging.config  # needed when logging_config doesn't start with logging.config
import sys


class LoggingMixin(object):
    logger = logging.getLogger('root')

    @property
    def logger(self):

        if self.debug:
            return logging.getLogger('KE-py-debug')
        else:
            return logging.getLogger('root')


DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(asctime)-15s %(name)s  %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'simple'
        },
    },
    'loggers': {
        'root': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': True,
        },
        'KE-py-debug': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': True,
        }
    }
}


def configure_logging(logging_settings=None):
    """you should use: configure_logging(settings.LOGGING)"""
    if not logging_settings:
        logging.config.dictConfig(DEFAULT_LOGGING)
    else:
        logging.config.dictConfig(logging_settings)
