from django.test import TestCase

from test_utils import create_test_user
from jetpack.models_old import Jet, JetVersion, Cap, CapVersion
from jetpack import settings

TEST_USERNAME = 'test_user'
TEST_JETPACK_NAME = 'test Jetpack'
TEST_CAP_NAME = 'test Capability'

class JetpackTest(TestCase):

	def setUp(self):
		self.to_delete = []
		self.user = create_test_user(username=TEST_USERNAME)
		self.jetpack = Jet(name=TEST_JETPACK_NAME, creator=self.user)
		self.jetpack.save()
		self.version = JetVersion(jetpack=self.jetpack, name='first', author=self.user)
		self.version.save()

	def tearDown(self):
		self.user.delete()
		for o in self.to_delete:
			try:
				o.delete()
			except:
				print "Object %s can't be deleted" % str(o)

	def test_jetpack_creation(self):
		jetpack = Jet.objects.get(name=TEST_JETPACK_NAME)
		self.failUnless(jetpack)

	def test_first_as_base(self):
		"""
		First is base
		"""
		# first created version is base one
		self.failUnless(self.jetpack.base_version)
		self.assertEqual(self.jetpack.base_version.name, 'first')

	def test_version_numbering(self):
		self.assertEqual(self.jetpack.base_version.fullname, 'first.0')

	def test_switch_base(self):
		"""
		There is only one base version per Jetpack
		"""
		# next base version 
		first_base_id = self.jetpack.base_version.id
		second_base = JetVersion(
			jetpack=self.jetpack, name='second', is_base=True, author=self.user
		)
		second_base.save()
		self.assertEqual(second_base.name, self.jetpack.base_version.name)
		
		first_base = JetVersion.objects.get(pk=first_base_id)
		self.assertEqual(first_base.is_base, False)

	def test_assign_capability(self):
		capability = Cap(name="Capability assigned", creator=self.user)
		capability.save()
		version = CapVersion(capability=capability, name='0.0', author=self.user)
		version.save()
		self.jetpack.base_version.capabilities.add(version)
		self.failUnless(version in self.jetpack.base_version.capabilities.all())
		
	def test_increase_counter(self):
		second_version=JetVersion(jetpack=self.jetpack, name='first', author=self.user)
		second_version.save()
		self.assertEqual(second_version.counter,1)

		
class CapabilityTest(TestCase):

	def setUp(self):
		self.to_delete = []
		self.user = create_test_user(username=TEST_USERNAME)
		self.capability = Cap(name=TEST_CAP_NAME, creator=self.user)
		self.capability.save()
		self.version = CapVersion(capability=self.capability, name='first', author=self.user)
		self.version.save()

	def tearDown(self):
		self.user.delete()
		for o in self.to_delete:
			try:
				o.delete()
			except:
				print "Object %s can't be deleted" % str(o)

	def test_capability_creation(self):
		capability = Cap.objects.get(name=TEST_CAP_NAME)
		self.failUnless(capability)

	def test_first_as_base(self):
		"""
		First is base
		"""
		# first created version is base one
		self.failUnless(self.capability.base_version)
		self.assertEqual(self.capability.base_version.name, 'first')

	def test_version_numbering(self):
		self.assertEqual(self.capability.base_version.fullname, 'first.0')

	def test_switch_base(self):
		"""
		There is only one base version per capability
		"""
		# next base version 
		first_base_id = self.capability.base_version.id
		second_base = CapVersion(
			capability=self.capability, name='second', is_base=True, author=self.user
		)
		second_base.save()
		self.assertEqual(second_base.name, self.capability.base_version.name)
		
		first_base = CapVersion.objects.get(pk=first_base_id)
		self.assertEqual(first_base.is_base, False)


	def test_assign_capability(self):
		capability = Cap(name="Capability assigned", creator=self.user)
		capability.save()
		version = CapVersion(capability=capability, name='0.0', author=self.user)
		version.save()
		self.capability.base_version.capabilities.add(version)
		self.failUnless(version in self.capability.base_version.capabilities.all())
		

	def test_increase_counter(self):
		# assert save with given counter does not change it
		self.version.save()
		self.assertEqual(self.version.counter, 0)
		# assert save without given counter sets it automatically
		second_version=CapVersion(capability=self.capability, name='first', author=self.user)
		second_version.save()
		self.assertEqual(second_version.counter,1)

