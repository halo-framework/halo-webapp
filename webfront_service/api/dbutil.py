
import logging
import datetime
from datetime import timedelta
import json
import uuid


from halo_app.exceptions import HaloError
from halo_app.logs import log_json
# mixin
from .mixin.mixin_db import *
from .models import *


logger = logging.getLogger(__name__)

tbl = False


class DbUtil(DbMixin):

	def __init__(self, req_context):
		super(DbUtil, self).__init__(req_context)
		try:
			logger.debug('start db setup')
			self.setup()
			logger.debug('finish db setup')
		except Exception as e:
			logger.error(str(e), extra=log_json(req_context))
			raise HaloError("error in db setup:"+str(e))

	def setup(self):
		global tbl
		tbl = True


		            

