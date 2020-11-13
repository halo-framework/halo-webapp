#!/usr/bin/env python
import logging
import json
from click.testing import CliRunner
from halo_app.exceptions import HaloError
from halocli.cli import start,cli
import os
import tempfile
import uuid
from halo_app.classes import AbsBaseClass
from .util import Util
from halo_app.settingsx import settingsx

settings = settingsx()

logger = logging.getLogger(__name__)


def generate(config,swagger):
    dir_tmp = tempfile.TemporaryDirectory()
    dir_name = dir_tmp.name

    uuid2 = uuid.uuid4().__str__()
    swagger_file_path = os.path.join(dir_name, uuid2)
    swagger_file = open(swagger_file_path, "w+")
    swagger_file.write(json.dumps(swagger))
    swagger_file.close()

    services = []
    for s in config['mservices']:
        services.append(s)
        #config['mservices'][s]['urls'] = swagger_file_path
        config['mservices'][s]['record']['path'] = swagger_file_path

    uuid1 = uuid.uuid4().__str__()
    config_file_path = os.path.join(dir_name, uuid1)
    config_file = open(config_file_path, "w+")
    config_file.write(json.dumps(config))
    config_file.close()

    service_name = services[0]
    #arr = ['--debug','-s',config_file_path,'extend', 'swagger','-f', 'fields','-s','halo_credit_charge_card', '-p', dir_name]
    arr = ['--debug','-s',config_file_path,'extend', 'swagger','-s', service_name, '-p', dir_name,'-a','all']
    cl = start(False, arr)
    runner = CliRunner()
    print('test_cli_base:'+str(arr))
    result = runner.invoke(cl, arr)
    print('r=' + str(result))
    print("output:" + str(result.output))
    if result.exit_code == 0:
        #print("error:"+str(result.stderr))
        text_files = [f for f in os.listdir(dir_name) if f.endswith('_extend.json')]
        print(text_files)
        if len(text_files) == 1:
            extend_file_path = os.path.join(dir_name, text_files[0])
            with open(extend_file_path, "r+") as f:
                data = f.read()
                print("finished extend:"+str(data))
                return data
    raise HaloError("extend failed")

class Extend(AbsBaseClass):
    def __init__(self,config,swagger):
        self.config = config
        self.swagger = swagger

    def generate(self):
        return generate(self.config,self.swagger)

if __name__ == '__main__':
    Extend("{'x':'y'}","halo-flask").generate()
