from django.conf.urls.defaults import *

urlpatterns = patterns('jetpack.views',
    url(r'^new/$','edit_new', name='jetpack_edit_new'),
    url(r'^jp(?P<slug>\w+)/$','edit_base', name='jetpack_edit_base'),
    url(r'^jp(?P<slug>\w+)/v(?P<version>.*)/$','edit_version', name='jetpack_edit_version'),
)

