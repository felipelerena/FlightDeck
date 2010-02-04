from django.contrib.auth.models import User
from person.models import Profile

class AMOAuthentication:

	def authenticate(self, username, password):
		"""
			Authenticate user by contacting with AMO
		"""
		
		# Try to retrieve AMO session info from db
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			user = None
		amo_session = None
		if user:
			amo_session = user.get_profile().amo_session

		# TODO: here contact AMO and receive authentication status
		authenticated = False
		if username != 'fake':
			authenticated = True

		# TODO: "steal" session cookie from AMO and save in profile
		amo_session = "fake"
		
		if not authenticated:
			return False

		# save user into the database
		if not user:
			user = User(
				username=username,
				password='saved in AMO',
				# TODO: retrieve from AMO
				first_name="John",
				last_name="Doe",
				email='fake@email.com' 
			)
			user.save()
		try:
			profile = user.get_profile()
		except Profile.DoesNotExist:
			profile = Profile()

		profile.amo_session = amo_session
		profile.save()

		return user
