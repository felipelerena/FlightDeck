from mechanize import Browser

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
		except User.DoesNotExist:
			user = None



		# TODO: here contact AMO and receive authentication status
		br = Browser()
		br.open("https://addons.mozilla.org/en-US/firefox/users/login?to=en-US")
		br.select_form(nr=2)
		br['data[Login][email]'] = username
		br['data[Login][password]'] = password

		response = br.submit()
		if response.geturl() != 'https://addons.mozilla.org/en-US/firefox':
			return None

		link = br.find_link(text='View Profile')
		email = username
		username = link.url.split('/')[-1]
		
		try:
			user = User.objects.get(username=username)
			if user.email != email:
				user.email = email
				user.save()
		except:
			# save user into the database
			user = User(
				username=username,
				email=email,
				password=DEFAULT_AMO_PASSWORD,
				# TODO: retrieve from AMO
				# first_name="John",
				# last_name="Doe",
				# email='fake@email.com' 
			)
			user.save()
		
		# save current amo_session if different
		try:
			profile = user.get_profile()
		except Profile.DoesNotExist:
			profile = Profile(user=user)
			profile.save()

		return user

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except:
			return None
