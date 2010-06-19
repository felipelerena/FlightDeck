from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseRedirect
from django.template import RequestContext#,Template
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from person.models import Profile
#from person.default_settings import settings

def public_profile(r, username, force=None):
	"""
	Public profile
	"""
	person = get_object_or_404(User, username=username)
	profile = person.get_profile()
	addons = person.packages_originated.filter(type='a')
	libraries = person.packages_originated.filter(type='l')
	# if owner of the profile and not specially wanted to see it - redirect to dashboard
	page = "profile"
	return render_to_response("profile.html", locals(),
				context_instance=RequestContext(r))

@login_required
def dashboard(r):
	"""
	Dashboard of the user
	"""
	page = "dashboard"
	person = r.user
	addons = r.user.packages_originated.filter(type='a')
	libraries = r.user.packages_originated.filter(type='l')
	return render_to_response("dashboard.html", locals(),
				context_instance=RequestContext(r))


