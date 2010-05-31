import os
import sys
from random import choice

from django.core.urlresolvers import reverse
from django.views.static import serve
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse, \
						HttpResponseForbidden, HttpResponseServerError
from django.template import RequestContext#,Template
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.views.decorators.http import require_POST

from base.shortcuts import get_object_or_create, get_object_with_related_or_404, get_random_string
from utils.os_utils import whereis

from jetpack.models import Package, PackageRevision, Module, Attachment
from jetpack import settings
from jetpack.package_helpers import get_package_revision
from jetpack.xpi_utils import xpi_remove 

def homepage(r):
	"""
	Get mixed packages for homepage
	"""
	return HttpResponse("Homepage here")

def package_browser(r, page_number=1, type=None, username=None):
	"""
	Display a list of addons or libraries with pages
	Filter based on the request (type, username).
	"""
	# calculate which template to use
	template_suffix = ''
	packages = Package.objects

	if username:
		author = User.objects.get(username=username)
		packages = packages.filter(author__username=username)
		template_suffix = '%s_user' % template_suffix
	if type: 
		other_type = 'l' if type == 'a' else 'a'
		other_packages_number = len(packages.filter(type=other_type))
		packages = packages.filter(type=type)
		template_suffix = '%s_%s' % (template_suffix, settings.PACKAGE_PLURAL_NAMES[type])

	limit = r.GET.get('limit', settings.PACKAGES_PER_PAGE)

	pager = Paginator(
		packages,
		per_page = limit,
		orphans = 1
	).page(page_number)
	

	return render_to_response(
		'package_browser%s.html' % template_suffix, locals(),
		context_instance=RequestContext(r))



def package_details(r, id, type, revision_number=None, version_name=None):
	"""
	Show package - read only
	"""
	revision = get_package_revision(id, type, revision_number, version_name)
	readonly = True
	return render_to_response("%s_view.html" % settings.PACKAGE_SINGULAR_NAMES[type], locals(),
				context_instance=RequestContext(r))
		

@login_required
def package_edit(r, id, type, revision_number=None, version_name=None):
	"""
	Edit package - only for the author
	"""
	revision = get_package_revision(id, type, revision_number, version_name)
	if r.user.pk != revision.author.pk:
		return HttpResponseForbidden('You are not the author of this Package')
	return HttpResponse('EDIT: %s' % revision)
		

@require_POST
@login_required
def package_create(r, type):
	"""
	Create new Package (Add-on or Library)
	Target of the Popup window with basic metadata
	"""
	item = Package(
		author=r.user,
		full_name=r.POST.get("full_name"),
		description=r.POST.get("description"),
		type=type
		)
	item.save()

	return render_to_response("json/%s_created.json" % settings.PACKAGE_SINGULAR_NAMES[type], {'item': item},
				context_instance=RequestContext(r),
				mimetype='application/json')

	
def package_create_xpi(r, id, revision_number=None, version_name=None):
	"""
	Edit package - only for the author
	"""
	revision = get_object_with_related_or_404(PackageRevision, 
						package__id_number=id, package__type='a',
						revision_number=revision_number)

	(stdout, stderr) = revision.build_xpi()

	if stderr and not settings.DEBUG:
		xpi_remove(sdk_dir)

	# return XPI url and cfx command stdout and stderr
 	return render_to_response('json/test_xpi_created.json', {
 					'stdout': stdout,
					'stderr': stderr,
 					'test_xpi_url': reverse('jp_test_xpi', 
									args=[
										revision.get_sdk_name(), 
										revision.package.get_unique_package_name(), 
										revision.package.name
										]), 
 					'download_xpi_url': reverse('jp_download_xpi', 
									args=[
										revision.get_sdk_name(), 
										revision.package.get_unique_package_name(), 
										revision.package.name
										]), 
 					'rm_xpi_url': reverse('jp_rm_xpi', args=[revision.get_sdk_name()])
 				},
				context_instance=RequestContext(r))
			#	mimetype='application/json')
	
def test_xpi(r, sdk_name, pkg_name, filename):
	"""
	return XPI file for testing
	"""
	path = '%s-%s/packages/%s' % (settings.SDKDIR_PREFIX, sdk_name, pkg_name)
	file = '%s.xpi' % filename 
	return serve(r, file, path, show_indexes=False)


def download_xpi(r, sdk_name, pkg_name, filename):
	"""
	return XPI file for testing
	"""
	path = '%s-%s/packages/%s' % (settings.SDKDIR_PREFIX, sdk_name, pkg_name)
	file = '%s.xpi' % filename 
	return serve(r, file, path, show_indexes=False)


def remove_xpi(r, sdk_name):
	xpi_remove('%s-%s' % (settings.SDKDIR_PREFIX, sdk_name))


