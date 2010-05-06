from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.template import RequestContext#,Template

from jetpack.views import homepage as jetpack_homepage

def homepage(r):
	return jetpack_homepage(r)
