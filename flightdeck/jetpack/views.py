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

def package_browser(r, page_number=1, type=None):
	"""
	Display a list of addons or libraries
	"""
	packages = Package.objects.filter(type=type)

	limit = r.GET.get('limit', settings.PACKAGES_PER_PAGE)

	pager = Paginator(
		packages,
		per_page = limit,
		orphans = 1
	).page(page_number)
	
	return render_to_response(
		'package_browser_%s.html' % settings.PACKAGE_PLURAL_NAMES[type], 
		{
			'page': 'packages',
			'pager': pager,
			'packages_name': settings.PACKAGE_PLURAL_NAMES[type],
			'type': type
		},
		context_instance=RequestContext(r))

def package_details(r, id, type, revision_number=None, version_name=None):

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

	return HttpResponse(package_revision.__unicode__())
		

