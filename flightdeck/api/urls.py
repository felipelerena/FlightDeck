from django.conf.urls.defaults import *

urlpatterns = patterns('api.views',
	url(r'', 'package', {'package_name': 'jetpack-core'},  name='api_home'),
	url(r'^package/(?P<package_name>.*)/module/(?P<module_name>.*)/$','module', name='api_module'),
	url(r'^package/(?P<package_name>.*)/$', 'package', name='api_package'),
)

