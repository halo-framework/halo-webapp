# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template
from flask_login import login_required

#blueprint = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')

# the views for project
# python
import datetime
import json
import logging
import urllib
import uuid
import requests
#flask
from flask import Response as HttpResponse
from flask import request
from flask.views import MethodView
# aws
from botocore.exceptions import ClientError
# common
#from halo_app.app.mixinx import PerfMixinX as PerfMixin
from halo_app.app.viewsx import AbsBaseLinkX as AbsBaseLinkY
# mixin
from .mixin.mixin_view import *
from .dbutil import DbUtil
from halo_app.settingsx import settingsx

settings = settingsx()

logger = logging.getLogger(__name__)

class AbsBaseLinkX(AbsBaseLinkY,MethodView):
	def process(self,method,args,headers):
		"""
        Return a list of all users.
        """

		if request.method == "GET":
			return self.process_get(request, args)

		if request.method == "POST":
			return self.process_post(request, args)

		if request.method == "PUT":
			return self.process_put(request, args)

		if request.method == "PATCH":
			return self.process_patch(request, args)

		if request.method == "DELETE":
			return self.process_delete(request, args)

		return HttpResponse('this is a ' + str(request.method))

class AbsBaseLink(AbsBaseLinkX):
	def get(self):
		ret = super(AbsBaseLink, self).do_process(request.path,request.args,request.headers)
		if ret and hasattr(ret, "code"):
			if ret.code == 200 and hasattr(ret, "type") and ret.type == "html":
				return ret.payload
			else:
				return "general error msg"
		return ret
		#return Util.json_data_response(ret.payload, ret.code, ret.headers)

	def post(self):
		data_dict = dict(request.args)
		data = request.get_json()
		data_dict['body'] = data
		ret = self.do_process(request.path,data_dict,request.headers)
		if ret and hasattr(ret, "code"):
			if ret.code == 200 and hasattr(ret, "type") and ret.type == "html":
				return ret.payload
			else:
				return "general error msg"
		return ret
		#return Util.json_data_response(ret.payload, ret.code, ret.headers)


class ErrorLink(ErrorMixin,AbsBaseLink):
	pass

class EditorLink(EditorMixin,AbsBaseLink):
	pass

class ListLink(ListMixin,AbsBaseLink):
	pass

class ExtendLink(ExtendMixin,AbsBaseLink):
	pass

class GenLink(GenMixin,AbsBaseLink):
	pass


class JsonLink(JsonMixin,AbsBaseLink):
	pass

from halo_app.app.mixinx import AbsBaseMixinX
from .mixin.mixin_handler import HandlerMixin


class EventLink__(AbsBaseMixinX, AbsBaseLink):
	def process_post(self, request, vars):
		event = request.data
		ctx = request.META
		handler = HandlerMixin()
		handler.get_event(event, ctx)
		return HttpResponse()