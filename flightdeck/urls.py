from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from flightdeck.base import views as base_views

try:
	import grappelli
	urls = [(r'^grappelli/', include('grappelli.urls'))]
except:
	urls = []


urls.extend([
	# Example:
	url(r'^$',base_views.placeholder, name='placeholder'),

	# docutils
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	# application
	(r'^admin/', include(admin.site.urls)),
])
urlpatterns = patterns('', *urls)
