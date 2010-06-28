import os
import sys
import time
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
from django.template.defaultfilters import slugify
from django.contrib import messages

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



def package_details(r, id, type, revision_number=None, version_name=None, latest=False):
	"""
	Show package - read only
	"""
	revision = get_package_revision(id, type, revision_number, version_name, latest)
	libraries = revision.dependencies.all()
	library_counter = len(libraries)
	if revision.package.is_addon():
		corelibrary = Package.objects.get(id_number=settings.MINIMUM_PACKAGE_ID)
		corelibrary = corelibrary.latest
		library_counter += 1
	readonly = True
	return render_to_response("%s_view.html" % revision.package.get_type_name(), locals(),
				context_instance=RequestContext(r))
		

@login_required
def package_copy(r, id, type, revision_number=None, version_name=None):
	"""
	Copy package - create a duplicate of the Package, set author as current user
	"""
	revision = get_package_revision(id, type, revision_number, version_name)
	""" it may be useful to copy your own package ...
	if r.user.pk == revision.author.pk:
		return HttpResponseForbidden('You are the author of this %s' % revision.package.get_type_name())
	"""

	try:
		package = Package.objects.get(
			full_name=revision.package.get_copied_full_name(), 
			author__username=r.user.username
			)
		return HttpResponseForbidden(
			'You already have a %s with that name' % revision.package.get_type_name()
			)
	except:
		package = revision.package.copy(r.user)
		revision.save_new_revision(package)

		return render_to_response("json/%s_copied.json" % package.get_type_name(), 
				{'revision': revision},
				context_instance=RequestContext(r),
				mimetype='application/json')
	

@login_required
def package_edit(r, id, type, revision_number=None, version_name=None, latest=False):
	"""
	Edit package - only for the author
	"""
	revision = get_package_revision(id, type, revision_number, version_name, latest)
	if r.user.pk != revision.author.pk:
		return HttpResponseRedirect(
					reverse("jp_%s_revision_details" % revision.package.get_type_name(), 
						args=[id, revision.revision_number])
					)
		#return HttpResponseForbidden('You are not the author of this Package')
		
	libraries = revision.dependencies.all()
	library_counter = len(libraries)
	if revision.package.is_addon():
		corelibrary = Package.objects.get(id_number=settings.MINIMUM_PACKAGE_ID)
		corelibrary = corelibrary.latest
		library_counter += 1

	return render_to_response("%s_edit.html" % revision.package.get_type_name(), locals(),
				context_instance=RequestContext(r))


@require_POST
@login_required
def package_add_module(r, id, type, revision_number=None, version_name=None):
	"""
	Add new module to the PackageRevision
	"""
	revision = get_package_revision(id, type, revision_number, version_name)
	if r.user.pk != revision.author.pk:
		return HttpResponseForbidden('You are not the author of this %s' % revision.package.get_type_name())

	filename = slugify(r.POST.get('filename'))

	mod = Module(
		filename=filename,
		author=r.user,
		code="""// %s.js - %s's module
// author: %s""" % (filename, revision.package.full_name, r.user.get_profile())
	)
	try:
		mod.save()
		revision.module_add(mod)
	except Exception, err:
		mod.delete()
		return HttpResponseForbidden(err)
		
	return render_to_response("json/module_added.json", 
				{'revision': revision, 'module': mod},
				context_instance=RequestContext(r),
				mimetype='application/json')

@require_POST
@login_required
def package_remove_module(r, id, type, revision_number):
	"""
	Remove module from PackageRevision
	"""
	revision = get_package_revision(id, type, revision_number)
	if r.user.pk != revision.author.pk:
		return HttpResponseForbidden('You are not the author of this Package')

	filename = r.POST.get('filename')

	modules = revision.modules.all()

	module_found = False

	for mod in modules:
		if mod.filename == filename:
			module = mod
			module_found = True

	if not module_found:
		return HttpResponseForbidden('There is no such module in %s' % revision.package.full_name)

	revision.module_remove(module)

	return render_to_response("json/module_removed.json", 
				{'revision': revision, 'module': module},
				context_instance=RequestContext(r),
				mimetype='application/json')


@require_POST
@login_required
def package_add_attachment(r, id, type, revision_number=None, version_name=None):
	"""
	Add new attachment to the PackageRevision
	"""
	revision = get_package_revision(id, type, revision_number, version_name)
	if r.user.pk != revision.author.pk:
		return HttpResponseForbidden('You are not the author of this %s' % revision.package.get_type_name())

	content = r.raw_post_data
	path = r.META.get('HTTP_X_FILE_NAME', False)

	if not path:
		return HttpResponseServerError

	filename, ext = os.path.splitext(path)
	ext = ext.split('.')[1].lower() if ext else ''

	upload_path = "%s_%s_%s.%s" % (revision.package.id_number, time.strftime("%m-%d-%H-%M-%S"), filename, ext)

	handle = open(os.path.join(settings.UPLOAD_DIR, upload_path), 'w')
	handle.write(content)
	handle.close()

	attachment = revision.attachment_create(
		author=r.user,
		filename=filename,
		ext=ext,
		path=upload_path
	)

	return render_to_response("json/attachment_added.json", 
				{'revision': revision, 'attachment': attachment},
				context_instance=RequestContext(r),
				mimetype='application/json')

@require_POST
@login_required
def package_remove_attachment(r, id, type, revision_number):
	"""
	Remove attachment from PackageRevision
	"""
	revision = get_package_revision(id, type, revision_number)
	if r.user.pk != revision.author.pk:
		return HttpResponseForbidden('You are not the author of this Package')

	filename = r.POST.get('filename','').strip()

	attachments = revision.attachments.all()

	attachment_found = False

	for att in attachments:
		if att.get_filename() == filename:
			attachment = att
			attachment_found = True

	if not attachment_found:
		return HttpResponseForbidden('There is no such attachment in %s' % revision.package.full_name)

	revision.attachment_remove(attachment)

	return render_to_response("json/attachment_removed.json", 
				{'revision': revision, 'attachment': attachment},
				context_instance=RequestContext(r),
				mimetype='application/json')


def download_attachment(r, path):
	"""
	Display attachment from PackageRevision
	"""
	
	attachment = get_object_or_404(Attachment, path=path)
	response = serve(r, path, settings.UPLOAD_DIR, show_indexes=False)
	#response['Content-Type'] = 'application/octet-stream';
	return response


@require_POST
@login_required
def package_save(r, id, type, revision_number=None, version_name=None):
	"""
	Save package and modules
	"""
	revision = get_package_revision(id, type, revision_number, version_name)
	if r.user.pk != revision.author.pk:
		return HttpResponseForbidden('You are not the author of this Package')

	reload = False
	save_revision = False
	save_package = False
	start_version_name = revision.version_name
	start_revision_message = revision.message
	start_revision_number = revision.revision_number

	response_data = {}

	package_full_name = r.POST.get('full_name', False)
	if package_full_name and package_full_name != revision.package.full_name:
		try:
			package = Package.objects.exclude(pk=package.pk).get(
				full_name=package_full_name, 
				type=revision.package.type,
				author__username=r.user.username,
				)
			return HttpResponseForbidden(
				'You already have a %s with that name' % revision.package.get_type_name()
				)
		except:
			save_package = True
			reload = True
			revision.package.full_name = package_full_name
			revision.package.name = None

	package_description = r.POST.get('package_description', False)
	if package_description:
		save_package = True
		revision.package.description = package_description
		response_data['package_description'] = package_description

	modules = []
	for mod in revision.modules.all():
		if r.POST.get(mod.filename, False):
			code = r.POST[mod.filename]
			if mod.code != code:
				mod.code = code
				modules.append(mod)

	if modules:
		revision.modules_update(modules)
		save_revision = False

	if save_revision:
		revision.save()

	revision_message = r.POST.get('revision_message', False)
	if revision_message and revision_message != start_revision_message:
		revision.message = revision_message
		" save revision message without changeing the revision "
		super(PackageRevision, revision).save()
		response_data['revision_message'] = revision_message

	version_name = r.POST.get('version_name', False)
	if version_name and version_name != start_version_name and version_name != revision.package.version_name:
		save_package = False
		try:
			revision.set_version(version_name)
		except Exception as err:
			return HttpResponseForbidden(err.__str__())

	if save_package:
		revision.package.save()
	
	response_data['version_name'] = revision.version_name if revision.version_name else ""

	if reload:
		response_data['reload'] = "yes"

	return render_to_response("package_saved.json", locals(),
				context_instance=RequestContext(r),
				mimetype='application/json')


def _get_full_name(full_name, username, type, i=0): 

	new_full_name = full_name

	if i > 0:
		new_full_name = "%s (%d)" % (full_name, i)

	packages = Package.objects.filter(author__username=username, full_name=new_full_name, type=type)

	if len(packages.all()) == 0:
		return new_full_name

	i = i + 1
	return _get_full_name(full_name, username, type, i)
	


@login_required
def package_create(r, type):
	"""
	Create new Package (Add-on or Library)
	Target of the Popup window with basic metadata
	"""

	full_name = r.POST.get("full_name", False)

	if full_name:
		description = r.POST.get("description")
		packages = Package.objects.filter(author__username=r.user.username, full_name=full_name, type=type)
		if len(packages.all()) > 0:
			return HttpResponseForbidden("You already have a %s with that name" % settings.PACKAGE_SINGULAR_NAMES[type])
	else:
		description = ""
		full_name = 'My Add-on' if type == 'a' else 'My Library'
		full_name = _get_full_name(full_name, r.user.username, type)


	item = Package(
		author=r.user,
		full_name=full_name,
		description=description,
		type=type
		)
	item.save()

	return HttpResponseRedirect(reverse('jp_%s_edit_latest' % item.get_type_name(), args=[item.id_number]))
	"""
	return render_to_response("json/%s_created.json" % item.get_type_name(), {'item': item},
				context_instance=RequestContext(r),
				mimetype='application/json')
	"""


@login_required
def library_autocomplete(r):
	"""
	'Live' search by name
	"""
	try:
		query = r.GET.get('q')
		limit = r.GET.get('limit', settings.LIBRARY_AUTOCOMPLETE_LIMIT)
		found = Package.objects.filter(type='l').exclude(name='jetpack-core').filter(
					Q(name__icontains=query) | \
					Q(full_name__icontains=query)
					)[:limit]
	except:
		found = []

	return render_to_response('json/library_autocomplete.json',
				{'libraries': found},
				context_instance=RequestContext(r),
				mimetype='application/json')


@require_POST
@login_required
def package_assign_library(r, id, type, revision_number=None, version_name=None):
	" assign library to the package "
	revision = get_package_revision(id, type, revision_number, version_name)
	if r.user.pk != revision.author.pk:
		return HttpResponseForbidden('You are not the author of this Package')

	library = get_object_or_404(Package, type='l', id_number=r.POST['id_number'])
	if r.POST.get('use_latest_version', False):
		lib_revision = library.version
	else:
		lib_revision = library.latest

	try:
		revision.dependency_add(lib_revision)
	except Exception as err:
		return HttpResponseForbidden(err.__str__())
		

	lib_revision_url = lib_revision.get_edit_url() \
		if r.user.pk == lib_revision.pk \
		else lib_revision.get_absolute_url()


	return render_to_response('json/library_assigned.json',
				locals(),
				context_instance=RequestContext(r),
				mimetype='application/json')


@require_POST
@login_required
def package_remove_library(r, id, type, revision_number):
	" remove dependency from the library provided via POST "
	revision = get_package_revision(id, type, revision_number)
	if r.user.pk != revision.author.pk:
		return HttpResponseForbidden('You are not the author of this %s' % revision.package.get_type_name())

	id_number = r.POST.get('id_number')
	library = get_object_or_404(Package, id_number=id_number)
	
	try:
		revision.dependency_remove_by_id_number(id_number)
	except Exception as err:
		return HttpResponseForbidden(err.__unicode__())
	
	return render_to_response('json/dependency_removed.json',
				{'revision': revision, 'library': library},
				context_instance=RequestContext(r),
				mimetype='application/json')
				




def get_revisions_list(id_number):
	" provide a list of the Package's revsisions "
	return PackageRevision.objects.filter(package__id_number=id_number)

def get_revisions_list_html(r, id_number):
	package = get_object_with_related_or_404(Package, id_number=id_number)
	revisions = get_revisions_list(id_number)
	return render_to_response(
		'_package_revisions_list.html', locals(),
		context_instance=RequestContext(r))




# ---------------------------- XPI ---------------------------------


def package_test_xpi(r, id, revision_number=None, version_name=None):
	"""
	Test XPI from data saved in the database
	"""
	revision = get_object_with_related_or_404(PackageRevision, 
						package__id_number=id, package__type='a',
						revision_number=revision_number)

	
	# support temporary data
	if r.POST.get('live_data_testing', False):
		modules = []
		for mod in revision.modules.all():
			if r.POST.get(mod.filename, False):
				code = r.POST[mod.filename]
				if mod.code != code:
					mod.code = code
					modules.append(mod)
		(stdout, stderr) = revision.build_xpi_test(modules)

	else:
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
	

def package_download_xpi(r, id, revision_number=None, version_name=None):
	"""
	Edit package - only for the author
	"""
	revision = get_object_with_related_or_404(PackageRevision, 
						package__id_number=id, package__type='a',
						revision_number=revision_number)

	(stdout, stderr) = revision.build_xpi()

	if stderr and not settings.DEBUG:
		xpi_remove(sdk_dir)

	return download_xpi(r, 
					revision.get_sdk_name(), 
					revision.package.get_unique_package_name(), 
					revision.package.name
					)


def test_xpi(r, sdk_name, pkg_name, filename):
	"""
	return XPI file for testing
	"""
	path = '%s-%s/packages/%s' % (settings.SDKDIR_PREFIX, sdk_name, pkg_name)
	file = '%s.xpi' % filename 
	mimetype='text/plain; charset=x-user-defined'

	return HttpResponse(open(os.path.join(path, file), 'rb').read(), mimetype=mimetype)



def download_xpi(r, sdk_name, pkg_name, filename):
	"""
	return XPI file for testing
	"""
	path = '%s-%s/packages/%s' % (settings.SDKDIR_PREFIX, sdk_name, pkg_name)
	file = '%s.xpi' % filename 
	response = serve(r, file, path, show_indexes=False)
	response['Content-Type'] = 'application/octet-stream';
	response['Content-Disposition'] = 'attachment; filename="%s.xpi"' % filename
	return response
 


def remove_xpi(r, sdk_name):
	xpi_remove('%s-%s' % (settings.SDKDIR_PREFIX, sdk_name))
	return HttpResponse('{}', mimetype='application/json')


