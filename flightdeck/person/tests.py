from django.test import TestCase
from django.contrib.auth.models import User

from person.models import Profile

class ProfileTest(TestCase):

	def setUp(self):
		self.user = User(
			username='jdoe',
			first_name='John',
			last_name='Doe'
		)
		self.user.save()

		self.profile = Profile()
		self.profile.user = self.user
		self.profile.nickname = 'doer'

		self.profile.save()
	
	def tearDown(self):
		self.profile.delete()
		self.user.delete()	

	def test_get_fullname(self):
		self.assertEqual(self.user.get_profile().get_fullname(), 'John Doe')
