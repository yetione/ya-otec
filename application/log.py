import logging
import logging.config
import logging.handlers


class Logger:
    def __init__(self, config=None):
        if config is None:
            config = self._get_default_config()
        self.set_config(config)

    @staticmethod
    def set_config(config):
        logging.config.dictConfig(config)


    @staticmethod
    def _get_default_config():
        return {
            'version': 1,
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'CRITICAL'
                },
                'debug': {
                    'class': 'logging.FileHandler',
                    'level': 'DEBUG',
                    'filename': './logs/debug.log',
                    'formatter': 'stdFormatter',
                },
                'info': {
                    'class': 'logging.FileHandler',
                    'level': 'INFO',
                    'filename': './logs/common.log',
                    'formatter': 'detailedFormatter',
                },
                'error': {
                    'class': 'logging.FileHandler',
                    'level': 'ERROR',
                    'filename': './logs/error.log',
                    'formatter': 'detailedFormatter',
                }
            },
            'formatters': {
                'detailedFormatter': {
                    'class': 'logging.Formatter',
                    'format': '%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s'
                },
                'stdFormatter': {
                    'class': 'logging.Formatter',
                    'format': '%(asctime)s %(name)-15s %(message)s'
                },
            },
            'loggers': {
                'shum': {
                    'level': 'DEBUG',
                    'handlers': ['debug', 'info', 'error']
                }
            },
            'root': {
                'handlers': ['console']
            },
        }


logger = Logger()
