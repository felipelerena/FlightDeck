from django.shortcuts import render_to_response, get_object_or_404
#from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext#,Template
from django.contrib.auth.decorators import login_required


from jetpack.models import Jetpack, Version
from jetpack.default_settings import settings

@login_required
def edit_new(r):
	return render_to_response('edit_new.html', {}, 
				context_instance=RequestContext(r))
	

@login_required
def edit_base(r, slug):
	jetpack = get_object_or_404(Jetpack, slug=slug)
	version = jetpack.base_version
	jetpack_page = True
	return render_to_response('edit.html', locals(), 
				context_instance=RequestContext(r))
	

@login_required
def edit_version(r, slug, version):
	version = get_object_or_404(Version, jetpack__slug=slug, name=version)
	jetpack = version.jetpack
	return render_to_response('edit.html', locals(), 
				context_instance=RequestContext(r))
	
