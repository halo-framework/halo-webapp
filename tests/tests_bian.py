from __future__ import print_function

import sys
import logging
from faker import Faker
from flask import Flask, request
from requests.auth import *
from flask_restful import Api
import json
import unittest
from halo_flask.exceptions import BadRequestError,ApiError
from halo_flask.flask.utilx import status
from halo_flask.apis import AbsBaseApi
from halo_flask.flask.utilx import Util
from halo_flask.flask.servicex import FoiBusinessEvent,SagaBusinessEvent
from halo_flask.flask.mixinx import InfoMixinX as InfoMixinX

try:
    from halo_webapp.webfront_service.api.mixin.mixin_view import StartMixin, PageMixin
except:
    from webfront_service.api.mixin.mixin_view import StartMixin, PageMixin


fake = Faker()
app = Flask(__name__)
app = Flask('__name__', template_folder="../webfront_service/templates/")
api = Api(app)



class MyBusinessEvent(FoiBusinessEvent):
    pass


class SaBusinessEvent(SagaBusinessEvent):
    pass


class A1(PageMixin):
    pass

class S1(InfoMixinX):
    pass

from flask import template_rendered
from contextlib import contextmanager

@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

class TestUserDetailTestCase(unittest.TestCase):
    """
    Tests /users detail operations.
    """

    def setUp(self):
        app.config.from_pyfile('../webfront_service/settings/local.py')
        #app.config.from_object('settings')
        logging.info('Setting up test: logged stdout')

    def tearDown(self):
        logging.info('tearDown test: logged stdout')

    def test_1_sp_request_returns_a_given_list(self):
        with app.test_request_context('/info'):
            self.s1 = S1()
            ret = self.s1.process_get(request, {})
            print("x=" + str(ret.payload))
            assert ret.code == status.HTTP_200_OK


    def test_2_load_proj_to_s3(self):
        with app.test_request_context('/info'):
            self.a1 = A1()
            ret = self.a1.process_get(request, {})
            print("x=" + str(ret.payload))
            assert ret.code == status.HTTP_200_OK


    def test_3_load_proj_to_s3(self):
        app.config['SSM_TYPE'] = "AWS"
        app.config['PROVIDER'] = "AWS"
        with app.test_request_context('/info'):
            self.a1 = A1()
            ret = self.a1.build_result("C:\dev\projects\halo\halo-webapp\serverless")
            print("x=" + str(ret))
            assert ret.status_code == status.HTTP_302_FOUND


    def test_1_get_request_returns_a_given_string(self):
        with app.test_request_context('/?name=Peter'):
            #import jinja2
            #app.jinja_loader = jinja2.FileSystemLoader('../webfront_service/templates')
            self.a1 = A1()
            ret = self.a1.process_get(request, {})
            assert ret.code == status.HTTP_200_OK

    def test_2_get_request_with_ref_returns_a_given_string(self):
        with app.test_request_context('/?name=Peter'):
            self.a1 = A1()
            ret = self.a1.process_get(request, {"cr_reference_id": "123"})
            assert ret.code == status.HTTP_200_OK



