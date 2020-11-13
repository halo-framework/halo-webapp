# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from webfront_service.extensions import login_manager
from webfront_service.utils import flash_errors
from ..api.views import settings


def load_public(app):
    stage = '/' + settings.ENV_NAME
    print("x="+str(stage))
    blueprint = Blueprint('public', __name__, static_folder='../static', url_prefix=stage)

    @blueprint.route('/', methods=['GET', 'POST'])
    def home():
        """Home page."""
        return render_template('public/home.html', the_content='this is halo')

    @blueprint.route('/about/')
    def about():
        """About page."""
        #form = LoginForm(request.form)
        return render_template('public/about.html')#, form=form)

    app.register_blueprint(blueprint)
