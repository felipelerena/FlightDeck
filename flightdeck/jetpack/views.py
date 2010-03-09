import os
import sys
import subprocess
from random import choice

from django.core.urlresolvers import reverse
from django.views.static import serve
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse, \
						HttpResponseNotAllowed, HttpResponseServerError
from django.template import RequestContext#,Template
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

from base.shortcuts import get_object_or_create
from utils.os_utils import whereis

from jetpack.models import Jet, JetVersion, Cap, CapVersion
from jetpack.default_settings import settings

def gallery(r, page=None, with_new=False):
	"""
	Display mixed list (Jetpacks with Capabilities)
	"""
	items = list(Jet.objects.all())
	items.extend(list(Cap.objects.all()))
	if not with_new:
		items = filter(lambda i: i.base_version, items)
	items.sort(lambda i, j: (j.base_version.last_update - i.base_version.last_update).seconds) 
	page = "packages"
	
	return render_to_response(
		'gallery.html', 
		locals(),
		context_instance=RequestContext(r))


@login_required
def jetpack_edit(r, slug):
	"""
	Get jetpack and send it to item_edit
	"""
	jetpack = get_object_or_404(Jet, slug=slug)
	return item_edit(r, jetpack, "jetpack")
	

@login_required
def capability_edit(r, slug):
	"""
	Get capability and send it to item_edit
	"""
	capability = get_object_or_404(Cap, slug=slug)
	return item_edit(r, capability, "capability")
	

def item_edit(r, item, type):
	"""
	retrieve item and (if possible) version 
	Render the right edit page for the given type
	"""
	try:
		version = item.base_version
	except: 
		#valid, as newly created item has no version yet
		pass
	if type == "jetpack":
		other_versions = JetVersion.objects.filter_by_slug(slug=item.slug)
	elif type == "capability":
		other_versions = CapVersion.objects.filter_by_slug(slug=item.slug)
 
	item_page = True
	page = "editor"
	jetpack_create_url = Jet.get_create_url()
	capability_create_url = Cap.get_create_url()
	return render_to_response("edit_item.html", locals(), 
				context_instance=RequestContext(r))
	

@login_required
def jetpack_version_edit(r, slug, version, counter):
	version = get_object_or_404(JetVersion, jetpack__slug=slug, name=version, counter=counter)
	item = version.jetpack
	type = "jetpack"
	page = "editor"
	other_versions = JetVersion.objects.filter_by_slug(slug=slug)
	return render_to_response('edit_item.html', locals(), 
				context_instance=RequestContext(r))
	

@login_required
def capability_version_edit(r, slug, version, counter):
	version = get_object_or_404(CapVersion, capability__slug=slug, name=version, counter=counter)
	item = version.capability
	other_versions = CapVersion.objects.filter_by_slug(slug=slug)
	type = "capability"
	page = "editor"
	return render_to_response('edit_item.html', locals(), 
				context_instance=RequestContext(r))


@login_required
def item_create(r, type):
	"""
	Create new item (Jetpack/Capability)
	This is a result of a popup window with just name and description
	Version will be saved in the item_version_create
	"""
	Klass = Jet if type=="jetpack" else Cap
	item = Klass(
		creator=r.user,
		name=r.POST.get("%s_name" % type),
		description=r.POST.get("%s_description" % type)
	)
	# TODO: validate
	item.save()
	return render_to_response("json/%s_created.json" % type, {type: item},
				context_instance=RequestContext(r),
				mimetype='application/json')
	
def item_get_versions(r, slug, type):
	"""
	get all existing versions for the item
	"""
	Klass = Jet if type=="jetpack" else Cap
	item = get_object_or_404(Klass, slug=slug)
	return render_to_response('json/versions.json', {
				"versions": item.versions.all()
			}, context_instance=RequestContext(r),
	)
	


@login_required
def item_update(r, slug, type):
	"""
	Update the existing item's metadata only
	"""
	Klass = Jet if type=="jetpack" else Cap
	item = get_object_or_404(Klass, slug=slug)
	if not item.can_be_updated_by(r.user):
		return HttpResponseNotAllowed(HttpResponse(""))

	if '%s_description' % type in r.POST:
		item.description = r.POST.get('%s_description' % type)
	if '%s_public_permission' % type in r.POST:
		item.public_permission = r.POST.get('%s_public_permission' % type)
	if '%s_group_permission' % type in r.POST:
		item.group_permission = r.POST.get('%s_group_permission' % type)

	item.save()
	return render_to_response('json/%s_updated.json' % type, {type: item},
				context_instance=RequestContext(r),
				mimetype='application/json')

	
@login_required
def item_version_create(r, slug, type):
	"""
	Save new version for the item, get data from POST
	"""
	if type == "jetpack":
		Klass = Jet 
		KlassVersion = JetVersion
	elif type == "capability":
		Klass = Cap
		KlassVersion = CapVersion

	item = get_object_or_404(Klass, slug=slug)
	version_data = {
		type: item,
		"author": r.user,
		"name": r.POST.get("version_name"),
		"content": r.POST.get("version_content"),
		"description": r.POST.get("version_description"),
	}
	if type == "jetpack":
		version_data["manifest"] = r.POST.get("version_manifest")

	if "version_status" in r.POST:
		version_data["status"] = r.POST.get("version_status")
	if "version_published" in r.POST:
		version_data["published"] = r.POST.get("version_published")
	if "version_is_base" in r.POST:
		version_data["is_base"] = r.POST.get("version_is_base")

	version = KlassVersion(**version_data)
	version.save()
	dep_capabilities = simplejson.loads(r.POST.get('capabilities','[]'));

	for c in dep_capabilities:
		dep_cap = CapVersion.objects.get(
						capability__slug=c['slug'],
						name=c['version'],
						counter=c['counter'])
		version.capabilities.add(dep_cap)

	return render_to_response('json/version_absolute_url.json', {'version': version},
				context_instance=RequestContext(r),
				mimetype='application/json')

@login_required
def item_version_update(r, slug, version, counter, type):
	"""
	Update the given version - no counter change
	"""
	if type == "jetpack":
		version = get_object_or_404(JetVersion, 
						jetpack__slug=slug, name=version, counter=counter)
	elif type == "capability":
		version = get_object_or_404(CapVersion, 
						capability__slug=slug, name=version, counter=counter)

	# permission check
	if not version.author == r.user:
		return HttpResponseNotAllowed(HttpResponse(""))

	version.author = r.user
	version.name = r.POST.get("version_name", version.name)
	if type == "jetpack":
		version.manifest = r.POST.get("version_manifest", version.manifest)
		version.published =  r.POST.get("version_published", version.published)
	version.content = r.POST.get("version_content", version.content)
	version.description = r.POST.get("version_description", version.description)
	version.status = r.POST.get("version_status", version.status)
	version.is_base = r.POST.get("version_is_base", version.is_base)
	version.save()
	return render_to_response('json/version_updated.json', {'version': version},
				context_instance=RequestContext(r),
				mimetype='application/json')
	
@login_required
def item_version_save_as_base(r, slug, version, counter, type):
	"""
	Update the given version - no counter change
	"""
	if type == "jetpack":
		version = get_object_or_404(JetVersion, 
						jetpack__slug=slug, name=version, counter=counter)
		item = version.jetpack
	elif type == "capability":
		version = get_object_or_404(CapVersion, 
						capability__slug=slug, name=version, counter=counter)
		item = version.capability

	# permission check
	if not item.can_be_updated_by(r.user):
		return HttpResponseNotAllowed(HttpResponse(""))

	version.is_base = True
	version.save()
	return render_to_response('json/version_saved_as_base.json', {'version': version},
				context_instance=RequestContext(r),
				mimetype='application/json')


##########################################################
# Manage dependencies

@login_required
def capabilities_autocomplete(r):
	"""
	Display names of the modules (capabilities) which mark the pattern
	"""
	
@login_required
def add_dependency(r, slug, type, version=None, counter=None):
	"""
	Add dependency to the item represented by slug
	"""
	# TODO: add more protection (do not allow two versions of the same Cap)
	if type == 'jetpack':
		item_version = get_object_or_404(JetVersion, 
					jetpack__slug=slug, name=version, counter=counter)
		item = item_version.jetpack
	elif type == 'capability':
		item_version = get_object_or_404(CapVersion, 
					capability__slug=slug, name=version, counter=counter)
		item = item_version.capability

	dependency_slug = r.POST.get("dependency_slug")
	dependency_version = r.POST.get("dependency_version", None)
	dependency_counter = r.POST.get("dependency_counter", None)
	if dependency_version:
		dependency = CapVersion.objects.get(
						capability__slug=dependency_slug, 
						name=dependency_version, 
						counter=dependency_counter)
		cap = dependency.capability
	else:
		cap = Cap.objects.get(slug=dependency_slug)
		dependency = cap.base_version

	item_version.capabilities.add(dependency)
	item_version.save()

	dependency_remove_url = reverse("jp_%s_remove_dependency" % type, args=[
		item.slug, item_version.name, item_version.counter,
		cap.slug, dependency.name, dependency.counter])

	return render_to_response('json/dependency_added.json', {
					'item': item_version, 
					'version': dependency, 
					'cap': dependency.capability,
					'dependency_remove_url': dependency_remove_url
				},
				context_instance=RequestContext(r),
				mimetype='application/json')
	
@login_required
def remove_dependency(r, slug, version, counter, type, d_slug, d_version, d_counter):
	"""
	Remove dependency from item
	"""
	if type == 'jetpack':
		item_version = get_object_or_404(JetVersion, 
					jetpack__slug=slug, name=version, counter=counter)
	elif type == 'capability':
		item_version = get_object_or_404(CapVersion, 
					capability__slug=slug, name=version, counter=counter)

	dependency = get_object_or_404(CapVersion,
					capability__slug=d_slug, name=d_version, counter=d_counter)

	item_version.capabilities.remove(dependency)
	item_version.save()
	return render_to_response('json/dependency_removed.json', locals(),
				context_instance=RequestContext(r),
				mimetype='application/json')


####################################################
# XPI CREATION

def create_xpi_from_post(r):
	"""
	Get all data needed for the XPI creation from POST
	call createXPI with the right data
	"""
	# all data has to be provided by POST
	slug = r.POST.get('jetpack_slug')
	main = r.POST.get('version_content')
	description = r.POST.get('jetpack_description')
	package = r.POST.get('version_manifest')
	libs = simplejson.loads(r.POST.get('capabilities'))

	return createXPI(r, slug, main, description, package, libs)

def createXPI(r, slug, main, description, package, libs):
	"""
	Create XPI from data given within POST
	Data will be cleaned by cron every x minutes
	No save is needed to createXPI
	"""
	if not whereis('cfx'):
		return HttpResponse('configuration error')

	# create random hash
	allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
	hash = 'jetpack-' + ''.join([choice(allowed_chars) for i in range(10)])

	# first create file structure
	os.mkdir ('/tmp/%s' % hash) 
	os.mkdir('/tmp/%s/lib' % hash)
	# chdir is needed as cfx is creating the xpi in current directory
	os.chdir('/tmp/%s' % hash)
	# prepare environment variables
	sys.path.append(settings.VIRTUAL_ENV)
	sys.path.append(settings.VIRTUAL_SITE_PACKAGES)


	for lib in libs:
		libHandle = open('/tmp/%s/lib/%s.js' % (hash, lib['slug']), 'w')
		libHandle.write(lib['version_content'])
		libHandle.close()

	
	pkgHandle = open('/tmp/%s/package.json' %hash, 'w')
	pkgHandle.write(package)
	pkgHandle.close()

	mainHandle = open('/tmp/%s/lib/main.js' % hash, 'w')
	mainHandle.write(main)
	mainHandle.close()

	descHandle = open('/tmp/%s/README.md' % hash, 'w')
	descHandle.write(description)
	descHandle.close()

	# save the directory using the hash only
	cfx_command = [
		'%s/scripts/cfx.sh' % settings.FRAMEWORK_PATH,
		'--binary=/usr/bin/xulrunner',
		'--pkgdir=/tmp/%s' % hash,
		'xpi'
	]

	try:
		process = subprocess.Popen(
						cfx_command, 
						shell=False, 
						stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	except subprocess.CalledProcessError:
		return HttpResponseServerError

	out = process.communicate()

	xpi_url = reverse('jp_get_xpi', args=[hash, slug])

	# return XPI url and cfx command stdout and stderr
	return render_to_response('json/xpi_created.json', {'xpi_url':xpi_url, 'out': out},
				context_instance=RequestContext(r),
				mimetype='application/json')
			

def getXPI(r, hash, slug):
	"""
	return XPI file
	"""
	return serve(r, '%s.xpi' % slug, '/tmp/%s' % hash, show_indexes=False)
