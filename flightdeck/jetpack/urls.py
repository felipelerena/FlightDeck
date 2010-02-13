from django.conf.urls.defaults import *

urlpatterns = patterns('jetpack.views',
    url(r'^new/$','edit_new', name='jetpack_edit_new'),
    url(r'^jp_(?P<slug>.*)/v_(?P<version>.*).(?P<counter>\d+)/$','edit_version', name='jetpack_edit_version'),
    url(r'^jp_(?P<slug>.*)/$','edit_base', name='jetpack_edit_base'),
)

