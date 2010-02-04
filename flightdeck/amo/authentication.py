from django.contrib.auth.models import User
from person.models import Profile

DEFAULT_AMO_PASSWORD = 'saved in AMO'

class AMOAuthentication:

	def authenticate(self, username, password):
		"""
			Authenticate user by contacting with AMO
		"""
		
		# Try to retrieve AMO session info from db
		try:
			user = User.objects.get(username=username)
			if user.password != DEFAULT_AMO_PASSWORD:
				" standard authorisation "		
				if user.check_password(password):
					return user
				return None
			amo_session = user.get_profile().amo_session
		except User.DoesNotExist:
			user = None
			amo_session = None



		# TODO: here contact AMO and receive authentication status
		authenticated = False
		if username != 'fake':
			authenticated = True

		# TODO: "steal" session cookie from AMO and save in profile
		amo_session = "fake"
		
		if not authenticated:
			return None

		# save user into the database
		if not user:
			user = User(
				username=username,
				password=DEFAULT_AMO_PASSWORD,
				# TODO: retrieve from AMO
				first_name="John",
				last_name="Doe",
				email='fake@email.com' 
			)
			user.save()
		
		# save current amo_session if different
		try:
			profile = user.get_profile()
		except Profile.DoesNotExist:
			profile = Profile(user=user)
		
		if amo_session != profile.amo_session:
			profile.amo_session = amo_session
			profile.save()

		return user
