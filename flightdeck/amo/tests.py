from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from person.models import Profile

class AuthTest(TestCase):
	
	def test_failing_login(self):
		# testing failed authentication on AMO
		self.assertEqual(
			None, 
			authenticate(
				username='non existing',
				password='user')
			)
