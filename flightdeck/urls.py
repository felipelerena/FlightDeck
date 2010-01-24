from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from flightdeck.base import views as base_views

urlpatterns = patterns('',

	# Example:
	url(r'^$',base_views.placeholder, name='placeholder'),

	### admin
	# grappelli
	(r'^grappelli/', include('grappelli.urls')),
	# docutils
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	# application
	(r'^admin/', include(admin.site.urls)),
)
