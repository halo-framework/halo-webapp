from flask import request
import time
import sys
import logging

from halo_app.settingsx import settingsx
settings = settingsx()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def start_timer():
    request.start_time = time.time()

def stop_timer(response):
    resp_time = time.time() - request.start_time
    logger.debug("Response time: %ss\n" % resp_time)
    return response

def record_request_data(response):
    logger.debug("Request path: %s Request method: %s Response status: %s\n" %
            (request.path, request.method, response.status_code))
    return response

def setup_metrics(app):
    app.before_request(start_timer)
    # The order here matters since we want stop_timer
    # to be executed first
    app.after_request(record_request_data)
    app.after_request(stop_timer)

