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

	# copy a PackageRevision
	url(r'^addon/copy/(?P<id>[-\w]+)/revision/(?P<revision_number>\d+)/$', 
		'package_copy', {'type': 'a'}, name='jp_addon_revision_copy'),
	url(r'^library/copy/(?P<id>[-\w]+)/revision/(?P<revision_number>\d+)/$', 
		'package_copy',{'type': 'l'},  name='jp_library_revision_copy'),

	# edit packagerevision
	url(r'^addon/edit/(?P<id>[-\w]+)/revision/(?P<revision_number>\d+)/$', 
		'package_edit', {'type': 'a'}, name='jp_addon_revision_edit'),
	url(r'^library/edit/(?P<id>[-\w]+)/revision/(?P<revision_number>\d+)/$', 
		'package_edit',{'type': 'l'},  name='jp_library_revision_edit'),


	# save packagerevision
	url(r'^addon/save/(?P<id>[-\w]+)/revision/(?P<revision_number>\d+)/$', 
		'package_save', {'type': 'a'}, name='jp_addon_revision_save'),
	url(r'^library/save/(?P<id>[-\w]+)/revision/(?P<revision_number>\d+)/$', 
		'package_save',{'type': 'l'},  name='jp_library_revision_save'),


	# test Add-on's PackageRevision
	url(r'^addon/test/(?P<id>[-\w]+)/revision/(?P<revision_number>\d+)/$', 
		'package_test_xpi', name='jp_addon_revision_test'),
	url(r'^addon/xpi/(?P<id>[-\w]+)/revision/(?P<revision_number>\d+)/$', 
		'package_download_xpi', name='jp_addon_revision_xpi'),
	
	# get and remove created XPI
	url(r'^addon/test_xpi/(?P<sdk_name>.*)/(?P<pkg_name>.*)/(?P<filename>.*)/$', 
		'test_xpi', name='jp_test_xpi'),
	url(r'^addon/download_xpi/(?P<sdk_name>.*)/(?P<pkg_name>.*)/(?P<filename>.*)/$', 
		'download_xpi', name='jp_download_xpi'),
	url(r'^addon/rm_xpi/(?P<sdk_name>.*)/$', 'remove_xpi', name='jp_rm_xpi'),
)

