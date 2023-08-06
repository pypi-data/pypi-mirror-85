import logging
import os
from dotenv import load_dotenv
load_dotenv(override=False)
from logging import config as logging_config

logger = logging.getLogger()


class Config:
    # Application
    APP_NAME = os.environ.get('APP_NAME')
    LOG_LEVEL = os.environ.get('LOG_LEVEL')
    ENVIRONMENT = os.environ.get('ENVIRONMENT')
    REGION = os.environ.get('REGION')

    # Email
    GMAIL_USER = os.environ.get('GMAIL_USER')
    GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')
    GMAIL_BYPRICE = os.environ.get('GMAIL_BYPRICE').split(',') if os.environ.get('GMAIL_BYPRICE') else None
    GMAIL_CC = os.environ.get('GMAIL_CC').split(',') if os.environ.get('GMAIL_CC') else None
    GMAIL_BCC = os.environ.get('GMAIL_BCC').split(',') if os.environ.get('GMAIL_BCC') else None
    GMAIL_HOST = os.environ.get('GMAIL_HOST')
    GMAIL_PORT = os.environ.get('GMAIL_PORT')


def init_app():
    global logger
    if not load_dotenv(override=False):
        logger.error('Could not find any .env file. The module will depend on system env only')

    # if application handlers , do nothing , else add just stdout handler
    if not logger.hasHandlers():
        app_logging_config = {
            'version': 1,
            'loggers': {
                '': {  # root logger
                    'level': os.getenv('LOG_LEVEL', 'INFO'),
                    'handlers': ['console'],
                },
            },
            'handlers': {
                'console': {
                    'level': os.getenv('LOG_LEVEL', 'INFO'),
                    'formatter': 'info',
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout',
                },
            },
            'formatters': {
                'info': {
                    'format': '%(asctime)s-%(module)s-%(lineno)s::%(levelname)s:: %(message)s'
                }
            },
        }

        logging_config.dictConfig(app_logging_config)
    logger.debug('emailconnection library initiated')


if __name__ == 'emailconnection':
    init_app()
