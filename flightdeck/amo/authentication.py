from mechanize import Browser
from BeautifulSoup import BeautifulSoup

from django.contrib.auth.models import User

from person.models import Profile, Limit
from amo import settings

DEFAULT_AMO_PASSWORD = 'saved in AMO'

class AMOAuthentication:

	def authenticate(self, username, password):
		"""
			Authenticate user by contacting with AMO
		"""
		
		# check if username exists in database
		try:
			user = User.objects.get(username=username)
			# was user signed up via AMO?
			if user.password != DEFAULT_AMO_PASSWORD:
				" standard authorisation "		
				if user.check_password(password):
					try:
						profile = user.get_profile()
					except:
						profile = Profile(user=user)
						profile.save()
					return user
				return None
		except User.DoesNotExist:
			user = None

		if settings.AMO_LIMITED_ACCESS:
			if username not in [x.email for x in list(Limit.objects.all())]:
				return None

		# here contact AMO and receive authentication status
		br = Browser()
		br.open("https://addons.mozilla.org/en-US/firefox/users/login?to=en-US")
		
		br.select_form(nr=2)
		br['data[Login][email]'] = username
		br['data[Login][password]'] = password

		response = br.submit()
		response_url = response.geturl()
		valid_urls = [
					'https://addons.mozilla.org/en-US/firefox/', 
					'https://addons.mozilla.org/en-US/firefox'
		]
		if not response_url in valid_urls:
			return None
		
		link = br.find_link(text='View Profile')
		email = username
		# retrieve username from the View Profile link
		# https://addons.mozilla.org/en-US/firefox/user/123456/
		# AMO developers once removed the trailing slash which has broken the database
		# all FD users had the username 'user'
		# following is to prevent such failure in the future
		if link.url[-1] != '/':
			username = link.url.split('/')[-1]
		else:
			username = link.url.split('/')[-2]

		if not username or username =='user':
			raise Exception("Problems with View Profile link")
			
		
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
			)
			user.save()
		
		# save current amo_session if different
		try:
			profile = user.get_profile()
		except Profile.DoesNotExist:
			# scrap initial profile data from AMO
			response = br.follow_link(text='Edit Profile')
			data = scrap_amo_profile(response)
			if 'firstname' in data:
				user.first_name = data['firstname']
			if 'lastname' in data:
				user.last_name = data['lastname']
			user.save()
			
			profile = Profile(user=user)
			if 'nickname' in data:
				profile.nickname = data['nickname']
			if 'location' in data:
				profile.location = data['location']
			if 'occupation' in data:
				profile.occupation = data['occupation']
			if 'homepage' in data:
				profile.homepage = data['homepage']
			if 'photo' in data:
				profile.homepage = data['photo']

			profile.save()

		return user

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except:
			return None


def scrap_amo_profile(response):
	soup = BeautifulSoup(response)
	data = {}
	for inp in soup.findAll('input'):
		try:
			if ('name', 'data[User][firstname]') in inp.attrs:
				data['firstname'] = inp['value']
			elif ('name','data[User][lastname]') in inp.attrs:
				data['lastname'] = inp['value']
			elif ('name', 'data[User][nickname]') in inp.attrs:
				data['nickname'] = inp['value']
			elif ('name', 'data[User][location]') in inp.attrs:
				data['location'] = inp['value']
			elif ('name','data[User][occupation]') in inp.attrs:
				data['occupation'] = inp['value']
			elif ('name', 'data[User][homepage]') in inp.attrs:
				data['homepage'] = inp['value']
		except:
			pass
	for img in soup.findAll('img'):
		classes = filter(lambda x: x[0] == 'class', img.attrs)
		alts = filter(lambda x: x[0] == 'alt', img.attrs)
		srcs = filter(lambda x: x[0] == 'src', img.attrs)
		if classes and alts and srcs:
			if 'avatar' in classes[0][1] and 'No photo' not in alts[0][1]:
				data['photo'] = 'https://addons.mozilla.org%s' % srcs[0][1]
	return data
