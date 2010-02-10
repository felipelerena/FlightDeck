from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext#,Template
from django.contrib.auth.models import User

from person.models import Profile
#from person.default_settings import settings

def public_profile(r, username):
	person = get_object_or_404(User, username=username)
	return HttpResponse("Here profile of %s" % str(person))
