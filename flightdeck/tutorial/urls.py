from django.conf.urls.defaults import *

urlpatterns = patterns('tutorial.views',
	url(r'^$', 'tutorial', name='tutorial'),
)
