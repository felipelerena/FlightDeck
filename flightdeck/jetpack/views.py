import os
import sys
from random import choice

from django.core.urlresolvers import reverse
from django.views.static import serve
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse, \
						HttpResponseNotAllowed, HttpResponseServerError
from django.template import RequestContext#,Template
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q

from base.shortcuts import get_object_or_create, get_object_with_related_or_404, get_random_string
from utils.os_utils import whereis

from jetpack.models import Package, PackageRevision, Module, Attachment
from jetpack import settings

def homepage(r):
	"""
	Get mixed packages for homepage
	"""
	return HttpResponse("Homepage here")

def package_browser(r, page_number=1, type=None, username=None):
	"""
	Display a list of addons or libraries
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


def get_package_revision(id, type, revision_number=None, version_name=None):

	if not (revision_number or version_name):
		# get default revision - one linked via Package:version
		package = get_object_with_related_or_404(Package, id_number=id, type=type)
		package_revision = package.version

	elif revision_number:
		# get version given by revision number
		package_revision = get_object_with_related_or_404(PackageRevision, 
							package__id_number=id, package__type=type,
							revision_number=revision_number)
	elif version_name:
		# get version given by version name
		package_revision = get_object_with_related_or_404(PackageRevision, 
							package__id_number=id, package__type=type,
							version_name=version_name)
	return package_revision


def package_details(r, id, type, revision_number=None, version_name=None):

	package_revision = get_package_revision(id, type, revision_number, version_name)
	return HttpResponse('VIEW: %s' % package_revision)
		
def package_edit(r, id, type, revision_number=None, version_name=None):

	package_revision = get_package_revision(id, type, revision_number, version_name)
	return HttpResponse('EDIT: %s' % package_revision)
		

