from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.template import RequestContext#,Template

from jetpack.models import Jet, Cap

def homepage(r):
	"""
	Display description of the website with a set of fresh stuff
	"""
	
	# TODO: filter out items without base version
	jet_limit = settings.HOMEPAGE_ITEMS_LIMIT+1
	jetpacks = Jet.objects.all()[:jet_limit]
	capabilities = Cap.objects.all()[:settings.HOMEPAGE_ITEMS_LIMIT]


	page = 'homepage'
	
	
	return render_to_response(
		'homepage.html', 
		locals(),
		context_instance=RequestContext(r))

