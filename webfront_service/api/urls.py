
import os
from flask import Response
#from halo_app.app.viewsx import PerfLinkX as PerfLink,HealthLinkX as HealthLink,InfoLinkX as InfoLink
from .views import EventLink__,ErrorLink,EditorLink,GenLink,ExtendLink,JsonLink


from halo_app.settingsx import settingsx

settings = settingsx()

def load_urls(app):
	stage = '/' + settings.ENV_NAME
	if 'AWS_LAMBDA_FUNCTION_NAME' in os.environ:
		stage = ""
	# system links
	app.add_url_rule(stage+'/robots.txt', view_func= lambda r: Response("User-agent: *\nDisallow: /", content_type="text/plain"))
	#app.add_url_rule(stage + '/perf', view_func=PerfLink.as_view('Perf'))
	#app.add_url_rule(stage + '/health', view_func=HealthLink.as_view('Health'))
	#app.add_url_rule(stage + '/info', view_func=InfoLink.as_view('Info'))
	#app.add_url_rule('/static/(?P<path>.*)$', DocRootLink.as_view('document_root'))
#	if settings.SERVER_LOCAL == True:
#		app.add_url_rule(stage+'/__event__/', view_func= EventLink__.as_view('_Event'))
	#app.add_url_rule(stage + '/500', view_func=ErrorLink.as_view('Error500'))


	#app.add_url_rule(stage + '/metrics/', view_func=MetricsLink.as_view('Metrics'))
	# app links
	app.add_url_rule(stage + '/editor', view_func=EditorLink.as_view('Editor'))
	app.add_url_rule(stage + '/api', view_func=JsonLink.as_view('Json'))
	app.add_url_rule(stage + '/extend', view_func=ExtendLink.as_view('Extend'))
	app.add_url_rule(stage + '/gen', view_func=GenLink.as_view('Generate'))
	#app.add_url_rule(stage + '/trans', view_func=TransLink.as_view('Trans'))








