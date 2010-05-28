from django.conf.urls.defaults import *

urlpatterns = patterns('jetpack.views',

	# browsing packages
	url(r'^addons/$', 'package_browser', {'type': 'a'}, name='jp_browser_addons'),
	url(r'^libraries/$', 'package_browser', {'type': 'l'}, name='jp_browser_libraries'),
	url(r'^addons/(?P<page_number>\d+)/$', 
		'package_browser', {'type': 'a'}, name='jp_browser_addons_page'),
	url(r'^libraries/(?P<page_number>\d+)/$', 
		'package_browser', {'type': 'l'}, name='jp_browser_libraries_page'),
	# by user
	url(r'^addons/by/(?P<username>\w+)/$', 
		'package_browser', {'type': 'a'}, name='jp_browser_user_addons'),
	url(r'^libraries/by/(?P<username>\w+)/$', 
		'package_browser', {'type': 'l'}, name='jp_browser_user_libraries'),
	url(r'^addons/by/(?P<username>\w+)/(?P<page_number>\d+)/$', 
		'package_browser', {'type': 'a'}, name='jp_browser_user_addons_page'),
	url(r'^libraries/by/(?P<username>\w+)/(?P<page_number>\d+)/$', 
		'package_browser', {'type': 'l'}, name='jp_browser_user_libraries_page'),

	# create new add-on/library
	url(r'^addon/new/',
		'package_create', {"type": "a"}, name='jp_addon_create'),
	url(r'^library/new/',
		'package_create', {"type": "l"}, name='jp_library_create'),


	# display details of the PackageRevision
	url(r'^addon/(?P<id>[-\w]+)/$', 
		'package_details', {'type': 'a'}, name='jp_addon_details'),
	url(r'^library/(?P<id>[-\w]+)/$', 
		'package_details',{'type': 'l'},  name='jp_library_details'),
	url(r'^addon/(?P<id>[-\w]+)/version/(?P<version_name>.*)/$', 
		'package_details', {'type': 'a'}, name='jp_addon_version_details'),
	url(r'^library/(?P<id>[-\w]+)/version/(?P<version_name>.*)/$', 
		'package_details',{'type': 'l'},  name='jp_library_version_details'),
	url(r'^addon/(?P<id>[-\w]+)/revision/(?P<revision_number>\d+)/$', 
		'package_details', {'type': 'a'}, name='jp_addon_revision_details'),
	url(r'^library/(?P<id>[-\w]+)/revision/(?P<revision_number>\d+)/$', 
		'package_details',{'type': 'l'},  name='jp_library_revision_details'),
	url(r'^addon/edit/(?P<id>[-\w]+)/revision/(?P<revision_number>\d+)/$', 
		'package_edit', {'type': 'a'}, name='jp_addon_revision_edit'),
	url(r'^library/edit/(?P<id>[-\w]+)/revision/(?P<revision_number>\d+)/$', 
		'package_edit',{'type': 'l'},  name='jp_library_revision_edit'),
)

