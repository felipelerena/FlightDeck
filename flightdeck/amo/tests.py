from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from person.models import Profile
from amo.authentication import DEFAULT_AMO_PASSWORD

class AuthTest(TestCase):
	def test_fake_authentication(self):
		"""
		test that any user except with username="fake" is authenticated
		"""
		# system should create and authenticate nonexisting user
		user = authenticate(username="username", password="password")
		self.failUnless(user)

		user = User.objects.get(username="username")
		self.assertEqual(user.password, DEFAULT_AMO_PASSWORD)
		self.failUnless(user.get_profile())
		self.assertEqual(user.get_profile().amo_session, 'fake')

	
	def test_fake_authentication_fail(self):
		"""
		authentication should fail if username="fake"
		"""
		user = authenticate(username="fake", password="password")
		self.assertEqual(user, None)

