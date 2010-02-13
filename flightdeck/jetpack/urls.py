from django.conf.urls.defaults import *

urlpatterns = patterns('jetpack.views',
	# Jetpacks
    url(r'^jp_new/$','jetpack_edit_new', name='jp_jetpack_edit_new'),
    url(r'^jp_(?P<slug>.*)/v_(?P<version>.*).(?P<counter>\d+)/$',
		'jetpack_edit_version', name='jp_jetpack_edit_version'),
    url(r'^jp_(?P<slug>.*)/$','jetpack_edit_base', name='jp_jetpack_edit_base'),
	# Capabilities
    url(r'^cap_new/$','capability_edit_new', name='jp_capability_new'),
    url(r'^cap_(?P<slug>.*)/v_(?P<version>.*).(?P<counter>\d+)/$',
		'capability_edit_version', name='jp_capability_edit_version'),
    url(r'^cap_(?P<slug>.*)/$','capability_edit_base', name='jp_capability_edit_base'),
)

