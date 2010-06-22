# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext#,Template

def tutorial(r):
	return render_to_response('tutorial.html',
			context_instance=RequestContext(r))
