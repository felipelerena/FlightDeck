from django.conf.urls.defaults import *

urlpatterns = patterns('jetpack.views',
	url(r'^addons/$', 'package_browser', {'type': 'a'}, name='jp_browser_addons'),
	url(r'^libraries/$', 'package_browser', {'type': 'l'}, name='jp_browser_libraries'),
)

