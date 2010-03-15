def profile(request):
	try:
	    return {'profile': request.user.get_profile()}
	except:
		return {}

