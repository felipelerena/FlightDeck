from django.conf.urls.defaults import *

urlpatterns = patterns('jetpack.views',
	url(r'^gallery/$', 'gallery', name='gallery'),

	url(r'^create_xpi/$', 'create_xpi_from_post', name='jp_create_xpi'),
	url(r'^get_xpi/(?P<hash>.*)/(?P<slug>.*)/$', 'getXPI', name='jp_get_xpi'),

    url(r'^ext_(?P<slug>.*)/v_(?P<version>.*)\.(?P<counter>\d+)/$',
		'jetpack_version_edit', name='jp_jetpack_version_edit'),
    url(r'^mod_(?P<slug>.*)/v_(?P<version>.*)\.(?P<counter>\d+)/$',
		'capability_version_edit', name='jp_capability_version_edit'),

	url(r'^extension/(?P<slug>.*)/versions/$', 
		'item_get_versions', {"type": "jetpack"}, name='jp_jetpack_get_versions'),
	url(r'^module/(?P<slug>.*)/versions/$', 
		'item_get_versions', {"type": "capability"}, name='jp_capability_get_versions'),

	url(r'^extension/(?P<slug>.*)/version/new/$', 
		'item_version_create', {"type": "jetpack"}, name='jp_jetpack_version_create'),
	url(r'^module/(?P<slug>.*)/version/new/$', 
		'item_version_create', {"type": "capability"}, name='jp_capability_version_create'),

	url(r'^extension/(?P<slug>.*)/v_(?P<version>.*)\.(?P<counter>\d+)/update/$', 
		'item_version_update', {"type": "jetpack"}, name='jp_jetpack_version_update'),
	url(r'^module/(?P<slug>.*)/v_(?P<version>.*)\.(?P<counter>\d+)/update/$', 
		'item_version_update', {"type": "capability"}, name='jp_capability_version_update'),

	url(r'^extension/(?P<slug>.*)/update/$', 
		'item_update', {"type": "jetpack"}, name='jp_jetpack_update'),
	url(r'^module/(?P<slug>.*)/update/$', 
		'item_update', {"type": "capability"}, name='jp_capability_update'),

	url(r'^extension/(?P<slug>.*)/v_(?P<version>.*)\.(?P<counter>\d+)/dependency/addnew/$',
		'addnew_dependency', {'type': 'jetpack'}, name='jp_jetpack_addnew_dependency'),
	url(r'^module/(?P<slug>.*)/v_(?P<version>.*)\.(?P<counter>\d+)/dependency/addnew/$',
		'addnew_dependency', {'type': 'capability'}, name='jp_capability_addnew_dependency'),

	url(r'^extension/(?P<slug>.*)/v_(?P<version>.*)\.(?P<counter>\d+)/dependency/add/$',
		'add_dependency', {'type': 'jetpack'}, name='jp_jetpack_add_dependency'),
	url(r'^module/(?P<slug>.*)/v_(?P<version>.*)\.(?P<counter>\d+)/dependency/add/$',
		'add_dependency', {'type': 'capability'}, name='jp_capability_add_dependency'),

	url(r'^extension/(?P<slug>.*)/v_(?P<version>.*)\.(?P<counter>\d+)/dependency/(?P<d_slug>.*)/v_(?P<d_version>.*)\.(?P<d_counter>\d+)/remove/$',
		'remove_dependency', {'type': 'jetpack'}, name='jp_jetpack_remove_dependency'),
	url(r'^module/(?P<slug>.*)/v_(?P<version>.*)\.(?P<counter>\d+)/dependency/(?P<d_slug>.*)/v_(?P<d_version>.*)\.(?P<d_counter>\d+)/remove/$',
		'remove_dependency', {'type': 'capability'}, name='jp_capability_remove_dependency'),

	url(r'^extension/(?P<slug>.*)/v_(?P<version>.*)\.(?P<counter>\d+)/set/base/$', 
		'item_version_save_as_base', {'type': 'jetpack'}, 
		name='jp_jetpack_version_save_as_base'),
	url(r'^module/(?P<slug>.*)/v_(?P<version>.*)\.(?P<counter>\d+)/set/base/$', 
		'item_version_save_as_base', {"type": "capability"}, 
		name='jp_capability_version_save_as_base'),

	url(r'^extension/new/',
		'item_create', {"type": "jetpack"}, name='jp_jetpack_create'),
	url(r'^module/new/',
		'item_create', {"type": "capability"}, name='jp_capability_create'),

    url(r'^ext_(?P<slug>.*)/$',
		'jetpack_edit', name='jp_jetpack_edit'),
    url(r'^mod_(?P<slug>.*)/$',
		'capability_edit', name='jp_capability_edit'),
)

