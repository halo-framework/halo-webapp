#!/usr/bin/env python
import logging
import urllib
import uuid
import datetime
import json
import tempfile
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
from io import BytesIO
import pkg_resources
from flask import redirect
# aws
from botocore.exceptions import ClientError
# common

# flask
from werkzeug import secure_filename
from flask import Response as HttpResponse, render_template,send_file,redirect,flash,jsonify
from wtforms import  BooleanField, StringField, PasswordField, validators,IntegerField,SelectField,SelectMultipleField
from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired, FileAllowed
# halo
from halo_app.app.utilx import Util as Utilx, strx#,Response
from halo_app.const import HTTPChoice
from halo_app.app.mixinx import AbsBaseMixinX as AbsBaseMixin
from halo_app.exceptions import HaloException,ApiError,BadRequestError,NoSuchPathException
from halo_app.logs import log_json
from halo_app.app.viewsx import AbsBaseLinkX as AbsBaseLink
from halo_app.response import HaloResponse
from halo_app.request import HaloRequest
#from halo.core import Halo
#from halo.core import Util as CoreUtil
#from halo.core import PROVIDER_LIST,RUNTIME_LIST
from ..dbutil import *
from ..apis import *
from ..events import *
from .logic.generate import Gen
from .logic.extend import Extend
from .logic.util import Util
from halo_app.settingsx import settingsx
settings = settingsx()

logger = logging.getLogger(__name__)

from webfront_service import __version__

VER = __version__

#@TODO 1. all proprietery code goes to mixin
#@TODO 2. add settings params to extend
#@TODO 3. add settings param data to .env
#@TODO 4. populate static dir
#@TODO 5. populate templates dir
#@TODO 6. add tests

dbaccess = None
def get_dbaccess(req_context):
    global dbaccess
    if dbaccess is None:
        dbaccess = DbUtil(req_context)
    return dbaccess

def get_event_dbaccess():
    req_context = Utilx.event_req_context
    dbaccess = DbUtil(req_context)
    return dbaccess

def bad_request_view(request):
    logger.debug('system-error 400')
    return HttpResponse(status=400)

def permission_denied_view(request):
    logger.error('system-error 403')
    return HttpResponse(status=403)

def page_not_found_view(request):
    logger.error('system-error 404')
    return HttpResponse(status=404)

def error_view(request):
    logger.error('system-error 500')
    return HttpResponse(status=500)

class ErrorMixin(AbsBaseMixin):

    def process_get(self, request, vars):
        ret = HaloResponse(HaloRequest(request))
        html = render_template("500.html")
        ret.payload = html
        ret.code = 200
        ret.headers = {}
        ret.type = "html"
        return ret


#@todo implement all features from front page:
#@todo Web filters for Analytics and more with chaining ability
#@todo Request monitoring with serverless dashboard or promateus
#@todo Request tracing and correlation id with log tool
#@todo Data mapping and obfuscation
#@todo Rest,Soap,RPC clients with connection pooling and timeout
#@todo Resiliency – Circuit Breaker
#@todo Logging & Exception Handling
#@todo Cloud & ONPREM support
#@todo Stateless architecture
#@todo Orchestration & SAGA
#@todo Service info & Health with custemization
#@todo persistance
#@todo security + jwt
#@todo 12 factor


class EditorMixin(AbsBaseMixin):

    def process_get(self, request, vars):
        """

                :param request:
                :param vars:
                :return:
                """
        ret = HaloResponse(HaloRequest(request))
        html = render_template("editor.html")
        ret.payload = html
        ret.code = 200
        ret.headers = {}
        ret.type = "html"
        return ret

class ExtendMixin(AbsBaseMixin):

    def process_post(self, request, vars):
        if 'conf' in vars['body']:
            conf = vars['body']['conf']
            config = json.loads(conf)
        if 'swgr' in vars['body']:
            swagger_content = vars['body']['swgr']
            swagger = json.loads(swagger_content)
            if config and swagger:
                extend = Extend(config,swagger)
                ret = extend.generate()
                return jsonify(ret)
        raise HaloError("no swagger content")

class GenMixin(AbsBaseMixin):

    def process_post(self, request, vars):
        if 'swagger' in request.form:
            swagger_content = request.form['swagger']
            swagger = json.loads(swagger_content)
            if swagger:
                if 'engine' in request.form:
                    engine = request.form['engine']
                else:
                    engine = 'halo-flask'
                if 'name' in request.form:
                    name = request.form['name']
                else:
                    name = 'project'
                gen = Gen(swagger, engine,name)
                return gen.generate()
        raise HaloError("no swagger content")


class AbsPageMixin(AbsBaseMixin):

    def get_sd_name(self,sd_id,ver='8'):
        BIAN_CONFIG = None
        if ver == '8':
            BIAN_CONFIG = settings.BIAN_CONFIG
        if ver == '9':
            BIAN_CONFIG = settings.BIAN_CONFIG9
        if sd_id in BIAN_CONFIG:
            return BIAN_CONFIG[sd_id]["name"]
        raise HaloError("no such id")


class JsonMixin(AbsPageMixin):

    def get_swagger_file_path(self,name,cb='false'):
        file_dir = os.path.dirname(__file__)
        fix_name = name.strip().replace("-", "_").replace(" ", "_")
        if cb:
            path = os.path.join(file_dir, '..', '..', '..', 'env', 'config', 'BIANV8X', name + ".json")
        else:
            path = os.path.join(file_dir, '..', '..', '..', 'env', 'config', 'BIANV8', name + ".json")
        clean_path = ''.join(c for c in path if c.isprintable())
        if not os.path.exists(clean_path):
            raise NoSuchPathException(clean_path)
        return clean_path

    def process_get(self, request, vars):
        """

        :param request:
        :param vars:
        :return:
        """
        ret = HaloResponse(HaloRequest(request))
        response_html = "generation failed. please try again"
        name = None
        headers = {}
        if 'sd_id' in vars:
            sd_id = vars['sd_id']
            if sd_id:
                if 'ver' in vars:
                    ver = vars['ver']
                    if ver:
                        if 'cb' in vars:
                            cb = vars['cb']
                            if cb:
                                name = self.get_sd_name(sd_id,ver)
                                swagger_file_path = self.get_swagger_file_path(name,cb)
                                return send_file(swagger_file_path)

