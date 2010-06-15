from django.conf.urls.defaults import *

urlpatterns = patterns('api.views',
	url(r'^(?P<package_name>[-\w]+)/module/(?P<module_name>[-\w]+)/$',
			'module', name='api_module'),
	url(r'^(?P<package_name>[-\w]+)/$', 'package', name='api_package'),
	url(r'$', 'homepage', name='api_home'),
)

