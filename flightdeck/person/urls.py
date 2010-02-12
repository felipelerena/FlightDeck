from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout


urlpatterns = patterns('person.views',
	url(r'^login/$', login, name='login'),
	url(r'^logout/$', logout, {"next_page": "/"}, name='logout'),
    url(r'^(?P<username>\w+)/$','public_profile', name='person_public_profile'),
)

