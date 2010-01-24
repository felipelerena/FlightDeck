from django.http import Http404, HttpResponseRedirect, HttpResponse

def placeholder(req):
	return HttpResponse("<h1>Hello World</h1>")
