from .settings import *


DEBUG = False
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
TEMPLATE_DEBUG = False
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'imagersite401@gmail.com'
EMAIL_HOST_PASSWORD = 'KkC4t!Nf<'
EMAIL_USE_TLS = True
EMAIL_TIMEOUT = None
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
