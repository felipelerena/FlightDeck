from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout


urlpatterns = patterns('person.views',
	url(r'^signin/$', login, name='login'),
	url(r'^signout/$', logout, {"next_page": "/"}, name='logout'),
    url(r'dashboard/$','dashboard', name='person_dashboard'),
    url(r'^(?P<username>\w+)/$','public_profile', name='person_public_profile'),
)

