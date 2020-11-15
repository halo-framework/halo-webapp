#!/usr/bin/env python
import logging
from jpype import startJVM, shutdownJVM, java, addClassPath, JClass, JInt,getDefaultJVMPath
import jpype.imports
import jpype
from jpype.types import *
from jpype import JImplements, JOverride,JImplementationFor
import os
import tempfile
import uuid
from halo_app.classes import AbsBaseClass
from .util import Util
from halo_app.settingsx import settingsx

settings = settingsx()

logger = logging.getLogger(__name__)

# set JRE_HOME or JAVA_HOME
# set working directory to project root

def generate(content,engine,name):
    #dir_name,uuidx = Util.set_dir()
    dir_tmp = tempfile.TemporaryDirectory()
    uuidx = uuid.uuid4().__str__()
    dir_name = dir_tmp.name
    swagger_file_path = os.path.join(dir_name, uuidx)
    swagger_file = open(swagger_file_path,"w+")
    swagger_file.write(content)
    swagger_file.close()
    #startJVM(getDefaultJVMPath(),"-ea", "-Djava.class.path=halo-flask-openapi-generator.jar;openapi-generator-cli.jar")
    if not jpype.isJVMStarted():
        #@todo make sure running directory is project root
        jars_dir = os.path.join(settings.BASE_DIR, '..','jars')
        jars_path = jars_dir+'/*'
        #jar_dir = os.path.join(os.getcwd(), 'jars')
        print("starting jvm:"+jars_path)
        startJVM("-ea", classpath=[jars_path], convertStrings=False)
    print(java.lang.System.getProperty('java.class.path'))
    addClassPath("org/openapitools/codegen")
    #from org.openapitools.codegen import OpenAPIGenerator
    jpype.JClass("org.openapitools.codegen.OpenAPIGenerator").main(['generate', '-g' ,engine, '-i', swagger_file_path,"-o",dir_name,"--package-name",name])
    print("finished generate")
    return Util.build_result(dir_name,name)

def finish_jvm():
    shutdownJVM()

class Gen(AbsBaseClass):
    def __init__(self,swagger_content,engine,name):
        self.swagger_content = swagger_content
        self.engine = engine
        self.name = name

    def generate(self):
        return generate(self.swagger_content,self.engine,self.name)

""""
@JImplements(java.lang.Runnable)
class MyShutdownHook:
    @JOverride
    def run(self):
       # perform any required shutdown activities
        print("Shutdown!!")

java.lang.Runtime.getRuntime().addShutdownHook(java.lang.Thread(MyShutdownHook()))
"""

if __name__ == '__main__':
    Gen("{'x':'y'}","halo-flask").generate()
