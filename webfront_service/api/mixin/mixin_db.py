#!/usr/bin/env python
import os
import logging
import datetime
import uuid
from pynamodb.exceptions import DoesNotExist,QueryError,PynamoDBException
from halo_app.exceptions import HaloException
from halo_app.app.utilx import strx
from halo_app.models import AbsDbMixin
from ..models import *
from halo_app.logs import log_json
from halo_app.settingsx import settingsx
settings = settingsx()

logger = logging.getLogger(__name__)


class DbMixin(AbsDbMixin):
	pass


