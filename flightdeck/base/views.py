from django.http import Http404, HttpResponseRedirect, HttpResponse

def placeholder(req):
	"""
	Display simple text. Just a proof the system is working

	@return HttpResponse: "<h1>Hello World</h1>"
	"""
	return HttpResponse("<h1>Hello World</h1>")
