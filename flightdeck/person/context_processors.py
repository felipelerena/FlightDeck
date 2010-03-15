def profile(request):
	if request.user.is_authenticated():
	    return {'profile': request.user.get_profile()}

