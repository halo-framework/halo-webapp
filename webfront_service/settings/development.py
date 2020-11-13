import os
from environs import Env
print("== start development")


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print('BASE_DIR : {}'.format(BASE_DIR))

env = Env()
THE_ENV=os.path.join(BASE_DIR,'..','env','.env.dev')
env.read_env(path=THE_ENV)
print('The .env file has been loaded. env: '+str(THE_ENV))

from webfront_service.settings.base import *

ENV_TYPE = DEV

ALLOWED_HOSTS = ['*','127.0.0.1',SERVER]

print('== The development settings file has been loaded.')