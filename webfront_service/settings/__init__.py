import os
import json
from halo_app.const import LOC,DEV,TST,PRD

print("== start init")

ENV_CONFIG = {LOC:LOC}
STAGE = LOC
STAGE_TYPE = LOC

if 'AWS_LAMBDA_FUNCTION_NAME' in os.environ:
    if 'HALO_STAGE' in os.environ:
        STAGE = os.environ['HALO_STAGE']
    if STAGE is not None:
        ENV_SETTINGS = 'env_settings.json'
        file_dir = os.path.dirname(__file__)
        file_path = os.path.join(file_dir,'..','..','env', ENV_SETTINGS)
        with open(file_path, 'r') as fi:
            API_CONFIG = json.load(fi)
            print("env_config:" + str(API_CONFIG))
        if STAGE in API_CONFIG:
            STAGE_TYPE = API_CONFIG[STAGE]
        else:
            raise Exception(file_path+" does not contain environment "+STAGE)

        if STAGE_TYPE == DEV:
            from .development import *
        else:
            if STAGE_TYPE == TST:
                from .test import *
            else:
                if STAGE_TYPE == PRD:
                    from .production import *
    else:
        raise Exception("can not get environment var HALO_STAGE")
else:
    from .local import *

print('== The init settings file has been loaded.')