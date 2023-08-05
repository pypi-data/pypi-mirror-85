"""
Solace PubSub+ Messaging API for Python Clients

This package contains a full-featured Python API for developing Python applications.  The API follows
the *builder* pattern.  Everything begins with a MessagingService.builder() which returns a new
`MessagingServiceClientBuilder` object.  With a `MessagingServiceClientBuilder` object, applications can:

- configure a :py:class:`solace.messaging.messaging_service.MessagingService` object
- create a :py:class:`solace.messaging.messaging_service.MessagingService` object
"""
import logging.config

from solace.messaging.core._solace_session import _SolaceApiLibrary

CORE_LIB = _SolaceApiLibrary().solclient_core_library
__all__ = ['messaging']
LOG_FILE = "solace_messaging_core_api.log"

SOLACE_LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'solace-messaging-formatter': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: [%(filename)s:%(lineno)s]  %(message)s'
        },
        'solace-messaging-core-api-formatter': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'NOTSET', # set to NOTSET to make all level log be handled
            'formatter': 'solace-messaging-formatter',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'core-api': {
            'level': 'NOTSET', # set to NOTSET to make all level log be handled
            'formatter': 'solace-messaging-core-api-formatter',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
    },
    'loggers': {
        'solace.messaging': {
            'handlers': ['default'],
            'level': 'WARNING',
            'propagate': False
        },
        'solace.messaging.publisher': {
            'handlers': ['default'],
            'level': 'WARNING',
            'propagate': False
        },
        'solace.messaging.receiver': {
            'handlers': ['default'],
            'level': 'WARNING',
            'propagate': False
        },
        'solace.messaging.connections': {
            'handlers': ['default'],
            'level': 'WARNING',
            'propagate': False
        },
        'solace.messaging.core': {
            'handlers': ['default'],
            'level': 'WARNING',
            'propagate': False
        },
        'solace.messaging.core.api': {
            'handlers': ['core-api'],
            'level': 'WARNING',
            'propagate': False
        }
    }
}

logging.config.dictConfig(SOLACE_LOGGING_CONFIG)
