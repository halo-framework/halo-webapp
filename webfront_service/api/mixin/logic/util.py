#!/usr/bin/env python
import tempfile
import uuid
import os
import logging
import urllib
import uuid
import datetime
import json
import tempfile
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
from io import BytesIO
from flask import redirect
from werkzeug import secure_filename
from flask import Response as HttpResponse, render_template,send_file
#from halo.core import Halo
#from halo.core import Util as CoreUtil
from halo_app.providers.providers import get_provider_name,ONPREM,get_provider
from halo_app.exceptions import HaloException,ApiError,BadRequestError,NoSuchPathException
from halo_app.classes import AbsBaseClass
from halo_app.settingsx import settingsx
from halo_app.classes import AbsBaseClass


settings = settingsx()

logger = logging.getLogger(__name__)

class Util(AbsBaseClass):
    @staticmethod
    def load_list(list):
        arr = []
        i = 1
        for p in list:
            arr.append({"id": i, "name": p})
            i = i + 1
        return arr

    @staticmethod
    def set_dir():
        dir_tmp = tempfile.TemporaryDirectory()
        uuidx = uuid.uuid4().__str__()
        dir = dir_tmp.name
        # Print current working directory
        print("Current working dir : %s" % dir)
        return dir,uuidx

    @staticmethod
    def build_result(dir_name,name="data"):
        memory_file = BytesIO()
        zip_name = name+".zip"
        # create a ZipFile object
        with ZipFile(memory_file, 'w', ZIP_DEFLATED) as zipObj:
            # Iterate over all the files in directory
            for folderName, subfolders, filenames in os.walk(dir_name):
                for filename in filenames:
                    # create complete filepath of file in directory
                    file_path = os.path.join(folderName, filename)
                    # create filepath of file in archive
                    arc_path = file_path[len(dir_name) + 1:]
                    # Add file to zip
                    zipObj.write(file_path,arc_path)
        memory_file.seek(0)
        if get_provider_name() != ONPREM:
            object_name = name+"-"+str(uuid.uuid4())[0:8]+".zip"
            print("object_name:" + object_name)
            bucket_name = settings.PROJ_BUCKET_NAME
            if get_provider().upload_file(memory_file,zip_name,bucket_name, object_name):
                url = get_provider().create_presigned_url(bucket_name, object_name, expiration=3600)
                print("url:"+url)
                return redirect(url, code=302)
        print("did it")
        return send_file(memory_file, attachment_filename=zip_name, as_attachment=True,mimetype='application/zip')