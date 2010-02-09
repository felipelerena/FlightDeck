from django.test import TestCase

from test_utils import create_test_user
from jetpack.models import Jetpack, Version
from jetpack import settings

TEST_USERNAME = 'test_user'
TEST_JETPACK_NAME = 'test Jetpack'

class JetpackTest(TestCase):

	def setUp(self):
		self.to_delete = []
		self.user = create_test_user(username=TEST_USERNAME)
		self.jetpack = Jetpack(name=TEST_JETPACK_NAME, author=self.user)
		self.jetpack.save()
		self.version = Version(jetpack=self.jetpack, name='first')
		self.version.save()

	def tearDown(self):
		self.user.delete()
		for o in self.to_delete:
			try:
				o.delete()
			except:
				print "Object %s can't be deleted" % str(o)

	def test_jetpack_creation(self):
		jetpack = Jetpack.objects.get(name=TEST_JETPACK_NAME)
		self.failUnless(jetpack)
		self.assertEqual(len(self.jetpack.slug), settings.JETPACK_SLUG_LENGTH);

	def test_first_as_base(self):
		"""
		First is base
		"""
		# first created version is base one
		self.failUnless(self.jetpack.base_version)
		self.assertEqual(self.jetpack.base_version.name, 'first')

	def test_switch_base(self):
		"""
		There is only one base version per Jetpack
		"""
		# next base version 
		first_base_id = self.jetpack.base_version.id
		second_base = Version(jetpack=self.jetpack, name='second', is_base=True)
		second_base.save()
		jetpack = Jetpack.objects.get(name=TEST_JETPACK_NAME)
		self.assertEqual(second_base.name, self.jetpack.base_version.name)
		
		first_base = Version.objects.get(pk=first_base_id)
		self.assertEqual(first_base.is_base, False)

		
