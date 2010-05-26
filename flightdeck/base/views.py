from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.template import RequestContext#,Template

from jetpack.models import Package
from jetpack import settings as jp_settings

def homepage(r):
	# one more for the main one 
	addons_limit = jp_settings.HOMEPAGE_PACKAGES_NUMBER + 1

	libraries = Package.objects.filter(type='l')[:jp_settings.HOMEPAGE_PACKAGES_NUMBER]
	addons = Package.objects.filter(type='a')[:addons_limit]

	addons = list(addons)
	featured = addons.pop(0)

	page = 'homepage'
	
	return render_to_response(
		'homepage.html', 
		locals(),
		context_instance=RequestContext(r))
