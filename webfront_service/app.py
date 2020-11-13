# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template
from flask_restful import Api, Resource, abort, reqparse
from flask_restful_swagger import swagger
from webfront_service import commands, public
from webfront_service.extensions import bcrypt, cache, csrf_protect, db, debug_toolbar, login_manager, migrate, webpack

if False:
    from webfront_service.helpers.middleware_adv import setup_metrics
else:
    from webfront_service.helpers.middleware import setup_metrics
api = None
def create_app(config_object='webfront_service.settings.__init__'):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)

    global api
    api = swagger.docs(
        Api(app),
        apiVersion="0.1",
        basePath="http://localhost:5000",
        resourcePath="/",
        produces=["application/json", "text/html"],
        api_spec_url="/api/spec",
        description="A Basic API",
    )
    print("swagger")

    register_halo(app)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    register_urls(app)
    register_monitor(app)
    return app

def register_halo(app):
    with app.app_context():
        from halo_app.apis import load_api_config
        if 'SSM_TYPE' in app.config and app.config['SSM_TYPE'] != 'NONE':
            load_api_config(app.config['ENV_TYPE'], app.config['SSM_TYPE'], app.config['FUNC_NAME'],
                            app.config['API_CONFIG'])

def register_monitor(app):
    setup_metrics(app)

def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    webpack.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    with app.app_context():
        from webfront_service.public.views import load_public
        load_public(app)
    #app.register_blueprint(public.views.blueprint)
    #app.register_blueprint(api.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': api.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)

def register_urls(app):
    from webfront_service.api import urls
    with app.app_context():
        urls.load_urls(app)
        if app.config["DEBUG"]:
            site_map(app)

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def site_map(app):
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = rule.rule
            links.append((url, rule.endpoint))
            print(str(url))

def at_exit():
    import atexit
    from webfront_service.api.mixin.logic.generate import finish_jvm
    #defining function to run on shutdown
    def close_jvm():
        finish_jvm()
        print("Threads complete, ready to finish")
    #Register the function to be called on exit
    atexit.register(close_jvm)
