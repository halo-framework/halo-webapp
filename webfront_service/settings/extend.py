#  settings for checkerservice project.



import os
from environs import Env
import re
import json

print("== start extend")

env = Env()

#add your vars below


BIAN_CONFIG = None
BIAN_SETTINGS = 'bian_settings.json'

file_dir = os.path.dirname(__file__)
file_path = os.path.join(file_dir,'..','..','env', BIAN_SETTINGS)
if os.path.exists(file_path):
    with open(file_path, 'r') as fi:
        BIAN_CONFIG = json.load(fi)
        print("bian_config:" + str(BIAN_CONFIG))
else:
    print("no bian config file")

LIBS = None
file_path = os.path.join(file_dir,'..','..','env', "libs.json")
if os.path.exists(file_path):
    with open(file_path, 'r') as fi:
        LIBS = json.load(fi)
        print("libs:" + str(LIBS))
else:
    print("no libs file")

CONSTS = None
file_path = os.path.join(file_dir,'..','..','env', "consts.json")
if os.path.exists(file_path):
    with open(file_path, 'r') as fi:
        CONSTS = json.load(fi)
        print("consts:" + str(CONSTS))
else:
    print("no consts file")

UPLOAD_FOLDER='/tmp/upload'
if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER,0o777)

MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16 MB

HALO_CONTEXT_LIST=[]
PROJ_BUCKET_NAME='halo-webapp-service-dev-projects'

ONPREM_PROVIDER_CLASS_NAME="ONPREMProvider"
ONPREM_PROVIDER_MODULE_NAME="halo_app.providers.providers"
ONPREM_SSM_CLASS_NAME='OnPremClient'
ONPREM_SSM_MODULE_NAME='halo_app.providers.ssm.onprem_ssm_client'

print('== The extend settings file has been loaded.')