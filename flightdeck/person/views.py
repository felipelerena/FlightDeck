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
	# if owner of the profile and not specially wanted to see it - redirect to dashboard
	if not force and username == r.user.username:
		return HttpResponseRedirect(reverse('person_dashboard'))
	page = "dashboard"
	return render_to_response("profile.html", locals(),
				context_instance=RequestContext(r))

@login_required
def dashboard(r):
	"""
	Dashboard of the user
	"""
	page = "dashboard"
	return render_to_response("dashboard.html", locals(),
				context_instance=RequestContext(r))
