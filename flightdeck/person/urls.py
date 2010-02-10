from django.conf.urls.defaults import *

urlpatterns = patterns('person.views',
    url(r'^(?P<username>\w+)/$','public_profile', name='person_public_profile'),
)

