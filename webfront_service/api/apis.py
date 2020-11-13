# the views for project
# python
import os
import datetime
import json
import logging
import urllib
import uuid
import requests
# aws
from botocore.exceptions import ClientError
# common
from halo_app.const import HTTPChoice
from halo_app.apis import AbsBaseApi
# flask
from halo_app.apis import SSM_APP_CONFIG
# DRF


logger = logging.getLogger(__name__)



class RecaptchaApi(AbsBaseApi):
	name = 'Recaptcha'


