from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed
from django.template import RequestContext#,Template
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

from base.shortcuts import get_object_or_create

from jetpack.models import Jet, JetVersion, Cap, CapVersion
from jetpack.default_settings import settings

@login_required
def create(r):
	"""
	Discplay create form
	"""
	jetpack_create_url = Jet.get_create_url()
	capability_create_url = Cap.get_create_url()
	return render_to_response('create.html', locals(), 
				context_instance=RequestContext(r))
	

@login_required
def jetpack_edit(r, slug):
	"""
	Get jetpack and (if possible) version 
	Render the edit page
	"""
	jetpack = get_object_or_404(Jet, slug=slug)
	try:
		version = jetpack.base_version
	except: 
		pass
	jetpack_page = True
	jetpack_create_url = Jet.get_create_url()
	capability_create_url = Cap.get_create_url()
	return render_to_response('jetpack_edit.html', locals(), 
				context_instance=RequestContext(r))
	

@login_required
def jetpack_version_edit(r, slug, version, counter):
	version = get_object_or_404(JetVersion, jetpack__slug=slug, name=version, counter=counter)
	jetpack = version.jetpack
	return render_to_response('jetpack_edit.html', locals(), 
				context_instance=RequestContext(r))
	

@login_required
def jetpack_create(r):
	"""
	Create new Jetpack
	This is a result of a popup window with just name and description
	Version will be saved in the jetpack_save_new_version
	"""
	jetpack = Jet(
		creator=r.user,
		name=r.POST.get("jetpack_name"),
		description=r.POST.get("jetpack_description")
	)
	# TODO: validate
	jetpack.save()
	return render_to_response('json/jetpack_created.json', {'jetpack': jetpack},
				context_instance=RequestContext(r),
				mimetype='application/json')
	
	

@login_required
def jetpack_update(r, slug):
	"""
	Update the existing Jetpack's metadata only
	"""
	jetpack = get_object_or_404(Jet, slug=slug)
	if not jetpack.can_be_updated_by(r.user):
		return HttpResponseNotAllowed(HttpResponse(""))

	# this is making too serious error 
	#assert jetpack.can_be_updated_by(r.user), \
	#	"You're not allowed to update this Jetpack"

	jetpack.description = r.POST.get('jetpack_description')
	if 'jetpack_public_permission' in r.POST:
		jetpack.public_permission = r.POST.get('jetpack_public_permission')
	if 'jetpack_group_permission' in r.POST:
		jetpack.group_permission = r.POST.get('jetpack_group_permission')
	jetpack.save()
	return render_to_response('json/jetpack_updated.json', {'jetpack': jetpack},
				context_instance=RequestContext(r),
				mimetype='application/json')
	
@login_required
def jetpack_version_create(r, slug):
	"""
	Save new version for the jetpack, get data from POST
	"""
	#TODO: save capabilities dependency
	jetpack = get_object_or_404(Jet, slug=slug)
	version_data = {
		"jetpack": jetpack,
		"author": r.user,
		"name": r.POST.get("version_name"),
		"manifest": r.POST.get("version_manifest"),
		"content": r.POST.get("version_content"),
		"description": r.POST.get("version_description"),
	}
	if "version_status" in r.POST:
		version_data["status"] = r.POST.get("version_status")
	if "version_published" in r.POST:
		version_data["published"] = r.POST.get("version_published")
	if "version_is_base" in r.POST:
		version_data["is_base"] = r.POST.get("version_is_base")
	version = JetVersion(**version_data)
	version.save()
	dep_capabilities = simplejson.loads(r.POST.get('capabilities','[]'));
	print dep_capabilities

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
def jetpack_version_update(r, slug, version, counter):
	"""
	Update the given version - no counter change
	"""
	version = get_object_or_404(JetVersion, jetpack__slug=slug, name=version, counter=counter)
	# permission check
	if not version.author == r.user:
		return HttpResponseNotAllowed(HttpResponse(""))

	version.author = r.user
	version.name = r.POST.get("version_name", version.name)
	version.manifest = r.POST.get("version_manifest", version.manifest)
	version.content = r.POST.get("version_content", version.content)
	version.description = r.POST.get("version_description", version.description)
	version.status = r.POST.get("version_status", version.status)
	version.published =  r.POST.get("version_published", version.published)
	version.is_base = r.POST.get("version_is_base", version.is_base)
	version.save()
	return render_to_response('json/version_updated.json', {'version': version},
				context_instance=RequestContext(r),
				mimetype='application/json')
	
@login_required
def jetpack_version_save_as_base(r, slug, version, counter):
	"""
	Update the given version - no counter change
	"""
	version = get_object_or_404(JetVersion, jetpack__slug=slug, name=version, counter=counter)
	# permission check
	if not version.jetpack.can_be_updated_by(r.user):
		return HttpResponseNotAllowed(HttpResponse(""))

	version.is_base = True
	version.save()
	return render_to_response('json/version_saved_as_base.json', {'version': version},
				context_instance=RequestContext(r),
				mimetype='application/json')


@login_required
def capability_edit(r, slug):
	capability = get_object_or_404(Cap, slug=slug)
	version = capability.base_version
	capability_page = True
	return render_to_response('capability_edit.html', locals(), 
				context_instance=RequestContext(r))
	

@login_required
def capability_version_edit(r, slug, version, counter):
	version = get_object_or_404(CapVersion, capability__slug=slug, name=version, counter=counter)
	capability = version.capability
	return render_to_response('capability_edit.html', locals(), 
				context_instance=RequestContext(r))
	
@login_required
def capability_create(r):
	"""
	Create new Capability
	This is a result of a popup window with just name and description
	Version will be saved in the capability_version_create
	"""
	# TODO: consider adding empty version here
	capability = Cap(
		creator=r.user,
		name=r.POST.get("capability_name"),
		description=r.POST.get("capability_description")
	)
	# TODO: validate
	capability.save()
	return render_to_response('json/capability_created.json', {'capability': capability},
				context_instance=RequestContext(r),
				mimetype='application/json')


@login_required
def capability_update(r, slug):
	"""
	Update the existing Capability's metadata only
	"""
	capability = get_object_or_404(Cap, slug=slug)
	if not capability.can_be_updated_by(r.user):
		return HttpResponseNotAllowed(HttpResponse(""))

	if 'capability_description' in r.POST:
		capability.description = r.POST.get('capability_description')
	if 'capability_public_permission' in r.POST:
		capability.public_permission = r.POST.get('capability_public_permission')
	if 'capability_group_permission' in r.POST:
		capability.group_permission = r.POST.get('capability_group_permission')
	capability.save()
	return render_to_response('json/capability_updated.json', {'capability': capability},
				context_instance=RequestContext(r),
				mimetype='application/json')
	
@login_required
def capability_version_create(r, slug):
	"""
	save new version for the capability, get data from POST
	"""
	#TODO: save capabilities dependency
	capability = get_object_or_404(Cap, slug=slug)
	version_data = {
		"capability": capability,
		"author": r.user,
		"name": r.POST.get("version_name"),
		"content": r.POST.get("version_content"),
		"description": r.POST.get("version_description"),
	}
	if "version_status" in r.POST:
		version_data["status"] = r.POST.get("version_status")
	if "version_is_base" in r.POST:
		version_data["is_base"] = r.POST.get("version_is_base")
	version = CapVersion(**version_data)
	version.save()
	return render_to_response('json/version_absolute_url.json', {'version': version},
				context_instance=RequestContext(r),
				mimetype='application/json')

@login_required
def capability_version_update(r, slug, version, counter):
	"""
	Update the given version - no counter change
	"""
	version = get_object_or_404(CapVersion, capability__slug=slug, name=version, counter=counter)
	# permission check
	if not version.author == r.user:
		return HttpResponseNotAllowed(HttpResponse(""))

	version.author = r.user
	if "version_name" in r.POST:
		version.name = r.POST.get("version_name", version.name)
	version.content = r.POST.get("version_content", version.content)
	if "version_description" in r.POST:
		version.description = r.POST.get("version_description", version.description)
	version.status = r.POST.get("version_status", version.status)
	version.is_base = r.POST.get("version_is_base", version.is_base)
	version.save()
	return render_to_response('json/version_updated.json', {'version': version},
				context_instance=RequestContext(r),
				mimetype='application/json')
	
@login_required
def capability_version_save_as_base(r, slug, version, counter):
	"""
	Update the given version - no counter change
	"""
	version = get_object_or_404(CapVersion, capability__slug=slug, name=version, counter=counter)
	# permission check
	if not version.capability.can_be_updated_by(r.user):
		return HttpResponseNotAllowed(HttpResponse(""))

	version.is_base = True
	version.save()
	return render_to_response('json/version_saved_as_base.json', {'version': version},
				context_instance=RequestContext(r),
				mimetype='application/json')


def gallery(r, page=None):
	"""
	Display mixed list (Jetpacks with Capabilities)
	"""
	items = list(Jet.objects.all()[0:20])
	items.extend(list(Cap.objects.all()[0:20]))
	items = filter(lambda i: i.base_version, items)
	items.sort(lambda i, j: (j.base_version.last_update - i.base_version.last_update).seconds) 
	
	return render_to_response(
		'gallery.html', 
		locals(),
		context_instance=RequestContext(r))
	

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
	if type == 'jetpack':
		item = JetVersion.objects.get(jetpack__slug=slug, name=version, counter=counter)
	elif type == 'capability':
		item = get_object_or_404(CapVersion, capability__slug=slug, name=version, counter=counter)

	dependency_slug = r.POST.get("dependency_slug")
	dependency_version = r.POST.get("dependency_version", None)
	dependency_counter = r.POST.get("dependency_counter", None)
	if dependency_version:
		dependency = CapVersion.objects.get(
						capability__slug=dependency_slug, 
						name=dependency_version, 
						counter=dependency_counter)
	else:
		cap = Cap.objects.get(slug=dependency_slug)
		dependency = cap.base_version

	item.capabilities.add(dependency)
	item.save()

	return render_to_response('json/dependency_added.json', {
					'item': item, 
					'version': dependency, 
					'cap': dependency.capability
				},
				context_instance=RequestContext(r),
				mimetype='application/json')
	
