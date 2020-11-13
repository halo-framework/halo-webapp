import os
from environs import Env
print("== start test")


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print('BASE_DIR : {}'.format(BASE_DIR))

env = Env()
THE_ENV=os.path.join(BASE_DIR,'..','env','.tst')
env.read_env(path=THE_ENV)
print('The .env file has been loaded. env: '+str(THE_ENV))

from webfront_service.settings.base import *

ENV_TYPE = TST

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'main_formatter': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                      '%(asctime)s; %(filename)s:%(lineno)d',
            'datefmt': "%Y-%m-%d %H:%M:%S",
            'class': "pythonjsonlogger.jsonlogger.JsonFormatter",
        },
        'main_formatter_old': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                      '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
    #    'file': {
    #        'level': 'DEBUG',
    #        'class': 'logging.FileHandler',
    #        'filename': '/path/to/django/debug.log',
    #    },
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
        'console_debug_false': {
            'level': 'DEBUG',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'formatter': 'main_formatter',
            'class': 'logging.StreamHandler'#'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': True,
        },
        'webfront_service.api.views': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'webfront_service.api.models': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'webfront_service.api.apis': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'webfront_service.api.events': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'webfront_service.handler': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_app.views': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_app.apis': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_app.events': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_app.mixin': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_app.models': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_app.util': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_app.ssm': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_app.saga': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'webfront_service.api.mixin.mixin_view': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'webfront_service.api.mixin.mixin_db': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'webfront_service.api.mixin.mixin_handler': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
    },
}


ALLOWED_HOSTS = ['127.0.0.1',SERVER]
INSTALLED_APPS += ['django_jenkins','django_extensions',]

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
    # 'django_jenkins.tasks.run_sloccount',
    # 'django_jenkins.tasks.run_graphmodels'
)

TEMPLATES[0]['OPTIONS']['debug'] = False

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'


print('== The test settings file has been loaded.')