#  settings for checkerservice project.


import os
from environs import Env
import json
from halo_app.const import LOC,DEV,TST,PRD

print("== start base")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = Env()

#ENV - flask environment
#ENV_TYPE - LOC,DEV,TST,PRD
#ENV_NAME - LOC or HALO_STAGE
#STAGE_URL - prefix for url

ENV = env.str('FLASK_ENV', default='production')
DEBUG = ENV == 'development'
SQLALCHEMY_DATABASE_URI = env.str('DATABASE_URL')
SECRET_KEY = env.str('SECRET_KEY')
BCRYPT_LOG_ROUNDS = env.int('BCRYPT_LOG_ROUNDS', default=13)
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False
CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
SQLALCHEMY_TRACK_MODIFICATIONS = False
WEBPACK_MANIFEST_PATH = 'webpack/manifest.json'
WTF_CSRF_CHECK_DEFAULT = False


ENV_TYPE = LOC

ENV_NAME = LOC

FUNC_NAME='webfront'

APP_NAME = 'webfront_service'

from .extend import *

#@TODO load config data from env var if possible and if not from env file
#@todo add coverage to project
SERVER_LOCAL = env.bool('SERVER_LOCAL', default=False)
AWS_REGION = env.str('AWS_REGION')
DB_URL = env.str('DYNAMODB_URL')
SECRET_JWT_KEY = env.str('SECRET_JWT_KEY')
STAGE_URL=env.bool('STAGE_URL',default=True)
SITE_NAME = env.str('SITE_NAME')

# SECURITY WARNING: keep the secret key used in production secret!
# Make this unique, and don't share it with anybody.
SECRET_KEY = env.str('SECRET_KEY')

###
#Given a version number MAJOR.MINOR.PATCH, increment the:
#
#MAJOR version when you make incompatible  changes,
#MINOR version when you add functionality in a backwards-compatible manner, and
#PATCH version when you make backwards-compatible bug fixes.
###

title='webfront'
author='Author'
copyright='Copyright 2017-2018 '+ author
major='1'
minor='1'
patch='52'
version=major+'.'+minor+'.'+patch
#year.month.day.optional_revision  i.e 2016.05.03 for today
rev=1
build='2018.10.10.'+str(rev)
generate='2019.09.28.18:27:36'
print("generate="+generate)

def get_version():
    """
    Return package version as listed in  env file
    """
    if ENV_TYPE == PRD:
        return version + "/" + build
    return version + "/" + build + "/" + generate+ ' (' + ENV_NAME + ')'

VERSION = get_version()
print(VERSION)

APPEND_SLASH = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)
print("DEBUG="+str(DEBUG))

SERVER = env.str('SERVER_NAME')
HALO_HOST = None

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DB_VER = env.str('DB_VER', default='0')
PAGE_SIZE = env.int('PAGE_SIZE', default=5)
def get_db():
    return {
        'default': env.db(),
    }
#DATABASES = get_db()

def get_cache():
  return {
      'default': env.cache()
    }
#CACHES = get_cache()

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause  to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
USE_TZ = True
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LOCALE_CODE = 'en-US'
LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', str('English')),
    #('nl', _('Dutch')),
    #('he', _('Hebrew')),
)

GET_LANGUAGE = True


LOCALE_PATHS = (
    os.path.join(BASE_DIR, '../locale'),
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

ROOT_URLCONF = 'webfront_service.urls'

CORS_ORIGIN_ALLOW_ALL = True


#STATIC_URL = '/static/'
STATIC_URL = "/"+ENV_NAME+'/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "api/static")

STATICFILES_DIRS = [
    #os.path.join(BASE_DIR, "api/static"),
    #'/var/www/static/',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
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
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
        'console_debug_false': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
        'mail_admins': {
            'level': 'ERROR',
            'formatter': 'main_formatter',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'webfront_service.api.views': {
            'level': 'DEBUG',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'webfront_service.api.models': {
            'level': 'DEBUG',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'webfront_service.api.apis': {
            'level': 'DEBUG',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'webfront_service.api.events': {
            'level': 'DEBUG',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'webfront_service.handler': {
            'level': 'DEBUG',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_app.flask.viewsx': {
            'level': 'DEBUG',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_app.apis': {
            'level': 'DEBUG',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_app.events': {
            'level': 'DEBUG',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_app.flask.mixinx': {
            'level': 'DEBUG',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_app.models': {
            'level': 'DEBUG',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_app.flask.utilx': {
            'level': 'DEBUG',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_app.ssm': {
            'level': 'DEBUG',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_app.saga': {
            'level': 'DEBUG',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'webfront_service.api.mixin.mixin_view': {
            'level': 'DEBUG',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'webfront_service.api.mixin.mixin_db': {
            'level': 'DEBUG',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'webfront_service.api.mixin.mixin_handler': {
            'level': 'DEBUG',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
    },
}
import logging.config
logging.config.dictConfig(LOGGING)

USER_HEADERS = 'Mozilla/5.0'

MIXIN_HANDLER = 'webfront_service.api.mixin.mixin_handler'

SERVICE_READ_TIMEOUT_IN_SC = 3  # in seconds = 300 ms

SERVICE_CONNECT_TIMEOUT_IN_SC = 3  # in seconds = 300 ms

RECOVER_TIMEOUT_IN_SC = 0.5  # in seconds = 500 ms

MINIMUM_SERVICE_TIMEOUT_IN_SC = 0.1  # in seconds = 100 ms

HTTP_MAX_RETRY = 4

THRIFT_MAX_RETRY = 4

HTTP_RETRY_SLEEP = 10 #0.100  # in seconds = 100 ms

ERR_MSG_CLASS = 'webfront_service.api.mixin.mixin_err_msg'

#in case a web edge
FRONT_WEB = False #env.str('FRONT_API',default=False)
file_dirname = os.path.dirname(__file__)
fr_file_path = os.path.join(file_dirname, "front_web.txt")
if os.path.exists(fr_file_path):
    FRONT_WEB = True
    # for screen messages

print ("FRONT_WEB:"+str(FRONT_WEB))

#in case an api edge
FRONT_API = False #env.str('FRONT_API',default=False)
file_dirname = os.path.dirname(__file__)
fr_file_path = os.path.join(file_dirname, "front_api.txt")
if os.path.exists(fr_file_path):
    FRONT_API = True
print ("FRONT_API:"+str(FRONT_API))

import uuid
INSTANCE_ID = uuid.uuid4().__str__()[0:4]

LOG_SAMPLE_RATE = 0.05 # 5%


SSM_TYPE = env.str('SSM_TYPE',default='NONE')
print('SSM_TYPE='+SSM_TYPE)

############################################################################################


API_CONFIG = None
API_SETTINGS = ENV_NAME + '_api_settings.json'

file_dir = os.path.dirname(__file__)
file_path = os.path.join(file_dir,'..','..','env','api', API_SETTINGS)
if os.path.exists(file_path):
    with open(file_path, 'r') as fi:
        API_CONFIG = json.load(fi)
        print("api_config:" + str(API_CONFIG))
else:
    print("no api config file")


BUSINESS_EVENT_MAP = None
EVENT_SETTINGS = ENV_NAME + '_event_settings.json'
file_dir = os.path.dirname(__file__)
file_path = os.path.join(file_dir,'..','..','env','config', EVENT_SETTINGS)
if os.path.exists(file_path):
    with open(file_path, 'r') as fi:
        map = json.load(fi)
        BUSINESS_EVENT_MAP = {}
        for key in map:
            val = map[key]
            print("val:"+key+" "+str(val))
            dict = {}
            for action in val:
                item = val[action]
                file_path_data = os.path.join(file_dir,'..','..','env','config', item['url'])
                print(file_path_data)
                with open(file_path_data, 'r') as fx:
                     data = json.load(fx)
                     dict[action] = { item['type'] : data }
            BUSINESS_EVENT_MAP[key] = dict


print('== The base settings file has been loaded.')