# -*- coding: utf-8 -*-
"""User models."""

import logging
import datetime
from datetime import timedelta
import json
import uuid


from halo_app.logs import log_json
from halo_app.models import AbsModel as Model
from halo_app.settingsx import settingsx
settings = settingsx()

logger = logging.getLogger(__name__)





ver = settings.DB_VER
uri = settings.DB_URL


          


