from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext#,Template
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

from base.shortcuts import get_object_or_create

from jetpack.models import Jet, JetVersion, Cap, CapVersion
from jetpack.default_settings import settings


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
	if not jetpack.can_by_updated_by(r.user):
		#TODO: raise NotAllowed or something
		return None

	jetpack.description = r.POST.get('ijetpack_description')
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
	if not (r.user.id == version.author.id or r.user in r.managers):
		# this should raise an error (HttpNotAllowed?)
		return None

	version.author = r.user
	version.name = r.POST.get("version_name", version.name)
	version.manifest = r.POST.get("version_manifest", version.manifest)
	version.content = r.POST.get("version_content", version.content)
	version.description = r.POST.get("version_description", version.description)
	version.status = r.POST.get("version_status", version.status)
	version.published =  r.POST.get("version_published", version.published)
	version.is_base = r.POST.get("version_is_base", version.is_base)
	version.save()
	return render_to_response('json/version_absolute_url.json', {'version': version},
				context_instance=RequestContext(r),
				mimetype='application/json')
	
@login_required
def jetpack_version_save_as_base(r, slug, version, counter):
	"""
	Update the given version - no counter change
	"""
	version = get_object_or_404(JetVersion, jetpack__slug=slug, name=version, counter=counter)
	# permission check
	if not (r.user.id == version.author.id or r.user in r.managers):
		# this should raise an error (HttpNotAllowed?)
		return None
	version.is_base = True
	version.save()
	return render_to_response('json/version_absolute_url.json', {'version': version},
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
		name=r.POST.get("capability_name"),
		description=r.POST.get("jetpackcapability")
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
	if not capability.can_by_updated_by(r.user):
		#TODO: raise NotAllowed or something
		return None

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
	if not (r.user.id == version.author.id or r.user in r.managers):
		# this should raise an error (HttpNotAllowed?)
		return None

	version.author = r.user
	version.name = r.POST.get("version_name", version.name)
	version.content = r.POST.get("version_content", version.content)
	version.description = r.POST.get("version_description", version.description)
	version.status = r.POST.get("version_status", version.status)
	version.is_base = r.POST.get("version_is_base", version.is_base)
	version.save()
	return render_to_response('json/version_absolute_url.json', {'version': version},
				context_instance=RequestContext(r),
				mimetype='application/json')
	
@login_required
def capability_version_save_as_base(r, slug, version, counter):
	"""
	Update the given version - no counter change
	"""
	version = get_object_or_404(CapVersion, capability__slug=slug, name=version, counter=counter)
	# permission check
	if not (r.user.id == version.author.id or r.user in r.managers):
		# this should raise an error (HttpNotAllowed?)
		return None
	version.is_base = True
	version.save()
	return render_to_response('json/version_absolute_url.json', {'version': version},
				context_instance=RequestContext(r),
				mimetype='application/json')
