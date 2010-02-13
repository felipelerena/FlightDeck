from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext#,Template
from django.utils import simplejson
from django.contrib.auth.decorators import login_required


from jetpack.models import Jet, JetVersion, Cap, CapVersion
from jetpack.default_settings import settings

@login_required
def jetpack_edit_new(r):
	return render_to_response('jetpack_edit_new.html', {}, 
				context_instance=RequestContext(r))
	

@login_required
def jetpack_edit_base(r, slug):
	jetpack = get_object_or_404(Jet, slug=slug)
	version = jetpack.base_version
	jetpack_page = True
	return render_to_response('jetpack_edit.html', locals(), 
				context_instance=RequestContext(r))
	

@login_required
def jetpack_edit_version(r, slug, version, counter):
	version = get_object_or_404(JetVersion, jetpack__slug=slug, name=version, counter=counter)
	jetpack = version.jetpack
	return render_to_response('jetpack_edit.html', locals(), 
				context_instance=RequestContext(r))
	
	
@login_required
def jetpack_save_new_version(r, slug):
	"""
	save new version for the jetpack, get data from POST
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
	return render_to_response('version_absolute_url.json', {'version': version},
				context_instance=RequestContext(r),
				mimetype='application/json')

@login_required
def jetpack_update_version(r, slug, version, counter):
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
	return render_to_response('version_absolute_url.json', {'version': version},
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
	return render_to_response('version_absolute_url.json', {'version': version},
				context_instance=RequestContext(r),
				mimetype='application/json')

@login_required
def capability_edit_new(r):
	return render_to_response('capability_edit_new.html', {}, 
				context_instance=RequestContext(r))
	

@login_required
def capability_edit_base(r, slug):
	capability = get_object_or_404(Cap, slug=slug)
	version = capability.base_version
	capability_page = True
	return render_to_response('capability_edit.html', locals(), 
				context_instance=RequestContext(r))
	

@login_required
def capability_edit_version(r, slug, version, counter):
	version = get_object_or_404(CapVersion, capability__slug=slug, name=version, counter=counter)
	capability = version.capability
	return render_to_response('capability_edit.html', locals(), 
				context_instance=RequestContext(r))
	
@login_required
def capability_save_new_version(r, slug):
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
	return render_to_response('version_absolute_url.json', {'version': version},
				context_instance=RequestContext(r),
				mimetype='application/json')

@login_required
def capability_update_version(r, slug, version, counter):
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
	return render_to_response('version_absolute_url.json', {'version': version},
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
	return render_to_response('version_absolute_url.json', {'version': version},
				context_instance=RequestContext(r),
				mimetype='application/json')
