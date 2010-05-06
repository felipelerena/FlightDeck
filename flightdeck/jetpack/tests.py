from django.test import TestCase

from test_utils import create_test_user
from jetpack.models import Package, PackageRevision
from jetpack import settings

TEST_USERNAME = 'test_user'
TEST_ADDON_NAME = 'test Addon'
TEST_ADDON_SLUG = 'test-addon'
TEST_LIBRARY_NAME = 'test Library'
TEST_LIBRARY_SLUG = 'test-library'
TEST_ADDON2_NAME = 'test Addon 2'

class PackageTest(TestCase):
	# self user, addon, library are created

	def test_addon_creation(self):
		addon = Package.objects.get(name=TEST_ADDON_NAME)
		self.failUnless(addon)

	def test_library_creation(self):
		library = Package.objects.get(name=TEST_LIBRARY_NAME)
		self.failUnless(library)

	def test_slug_creation(self):
		self.assertEqual(self.addon.slug, TEST_ADDON_SLUG)
		self.assertEqual(self.library.slug, TEST_LIBRARY_SLUG)

	def test_ordering(self):
		addon2 = Package(name=TEST_ADDON2_NAME, creator=self.user, type='a')
		addon2.save()
		self.to_delete.append(addon2)
		self.assertEqual(Package.objects.all()[0].name, TEST_ADDON2_NAME)
		
	def test_filtering(self):
		addon2 = Package(name=TEST_ADDON2_NAME, creator=self.user, type='a')
		addon2.save()
		self.to_delete.append(addon2)
		self.assertEqual(len(list((Package.objects.addons().all()))), 2)
		self.assertEqual(len(list((Package.objects.libraries().all()))), 1)

	def test_related_name(self):
		self.assertEqual(len(list(self.user.packages_originated.all())), 2)

	def setUp(self):
		self.to_delete = []
		self.user = create_test_user(username=TEST_USERNAME)
		self.addon = Package(
			name=TEST_ADDON_NAME, 
			creator=self.user, 
			type='a'
		)
		self.addon.save()
		self.to_delete.append(self.addon)
		self.library = Package(
			name=TEST_LIBRARY_NAME, 
			creator=self.user, 
			type='l'
		)
		self.library.save()
		self.to_delete.append(self.library)

	def tearDown(self):
		self.user.delete()
		for o in self.to_delete:
			try:
				o.delete()
			except:
				print 'Object %s can\'t be deleted' % str(o)

class PackageRevisionTest(TestCase):

	def setUp(self):
		self.to_delete = []
		self.user = create_test_user(username=TEST_USERNAME)
		self.addon = Package(name=TEST_ADDON_NAME, creator=self.user, type='a')
		self.addon.save()
		self.to_delete.append(self.addon)
		self.library = Package(name=TEST_LIBRARY_NAME, creator=self.user, type='l')
		self.library.save()
		self.to_delete.append(self.library)
		# signals have also created the first revisions

	def tearDown(self):
		self.user.delete()
		for o in self.to_delete:
			try:
				o.delete()
			except:
				print 'Object %s can\'t be deleted' % str(o)

	def test_first_revision(self):
		revisions = PackageRevision.objects.filter(package__slug=self.addon.slug)
		self.assertEqual(
			len(list(revisions)),
			1
		)
		revision = revisions[0]
		self.failUnless(revision.was_head)
		self.assertEqual(revision.owner.username, self.addon.creator.username)
		self.assertEqual(revision.revision_number, 0)
