import os
from environs import Env

print("== start local")


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print('BASE_DIR : {}'.format(BASE_DIR))

env = Env()
THE_ENV=os.path.join(BASE_DIR,'..','env','.env')
env.read_env(path=THE_ENV)
print('The .env file has been loaded. env: '+str(THE_ENV))

from webfront_service.settings.base import *

ENV_TYPE = LOC

ALLOWED_HOSTS = ['*','127.0.0.1',SERVER]

DEBUG_TOOLBAR_CONFIG = {
  'DISABLE_PANELS': [ 'debug_toolbar.panels.redirects.RedirectsPanel', ],
  'SHOW_TEMPLATE_CONTEXT': True,
}

INTERNAL_IPS = ['127.0.0.1', '192.168.0.1']

#get local urls for services
file_dir = os.path.dirname(__file__)
file_path = os.path.join(file_dir,'..','..','env', 'loc_settings.json')
if os.path.exists(file_path):
    with open(file_path, 'r') as fi:
        LOC_TABLE = json.load(fi)
        print("loc_settings:" + str(LOC_TABLE))
else:
    print("no loc_settings config file")

PROJ_BUCKET_NAME='halo-webapp-service-dev-projects'

print('== The local settings file has been loaded.')