from exceptions import TypeError

from django.test import TestCase

from test_utils import create_test_user
from jetpack.models import Package, PackageRevision, Module, Attachment
from jetpack import settings
from jetpack.errors import SelfDependencyException

TEST_USERNAME = 'test_user'
TEST_ADDON_NAME = 'test Addon'
TEST_ADDON_SLUG = 'test-addon'
TEST_LIBRARY_NAME = 'test Library'
TEST_LIBRARY_SLUG = 'test-library'
TEST_ADDON2_NAME = 'test Addon 2'
TEST_FILENAME = 'file-name'
TEST_FILENAME_EXTENSION = 'css'

class PackageTestCase(TestCase):
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



class PackageTest(PackageTestCase):
	# self user, addon, library are created

	def test_addon_creation(self):
		addon = Package.objects.get(name=TEST_ADDON_NAME)
		self.failUnless(addon)
		self.assertEqual(addon.id_number, settings.MINIMUM_PACKAGE_ID)


	def test_library_creation(self):
		library = Package.objects.get(name=TEST_LIBRARY_NAME)
		self.failUnless(library)
		self.assertEqual(library.id_number, settings.MINIMUM_PACKAGE_ID + 1)


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


	def test_directory_name(self):
		self.assertEqual(
			self.addon.get_directory_name(),
			"%s-%d" % (TEST_ADDON_SLUG, settings.MINIMUM_PACKAGE_ID)
		)


class PackageRevisionTest(PackageTestCase):

	def test_first_revision(self):
		revisions = PackageRevision.objects.filter(package__slug=self.addon.slug)
		self.assertEqual(1, len(list(revisions)))
		revision = revisions[0]
		self.assertEqual(revision.owner.username, self.addon.creator.username)
		self.assertEqual(revision.revision_number, 0)

	
	def test_save(self):
		# system should create new revision on save
		revisions = PackageRevision.objects.filter(package__slug=self.addon.slug)
		first = revisions[0]
		first.save()
		revisions = PackageRevision.objects.filter(package__slug=self.addon.slug)
		self.assertEqual(2, len(list(revisions)))

	
	def test_save_with_dependency(self):
		# system should copy on save with all dependencies
		first = PackageRevision.objects.filter(package__slug=self.addon.slug)[0]
		lib = PackageRevision.objects.filter(package__slug=self.library.slug)[0]
		first.dependencies.add(lib)
		first.save()

		first = PackageRevision.objects.filter(package__slug=self.addon.slug)[1]
		second = PackageRevision.objects.filter(package__slug=self.addon.slug)[0]
		self.assertEqual(second.dependencies.all()[0].package.slug, lib.package.slug)
		self.assertEqual(
			first.dependencies.all()[0].package.slug, 
			second.dependencies.all()[0].package.slug
		)


	def test_adding_addon_as_dependency(self):
		lib = PackageRevision.objects.filter(package__slug=self.library.slug)[0]
		addon = PackageRevision.objects.filter(package__slug=self.addon.slug)[0]
		self.assertRaises(TypeError, lib.dependency_add, addon)
		self.assertEqual(0, len(lib.dependencies.all()))


	def test_adding_library_to_itself_as_dependency(self):
		lib = PackageRevision.objects.filter(package__slug=self.library.slug)[0]
		self.assertRaises(SelfDependencyException, lib.dependency_add, lib)


	def test_adding_and_removing_dependency(self):
		first = PackageRevision.objects.filter(package__slug=self.addon.slug)[0]
		lib = PackageRevision.objects.filter(package__slug=self.library.slug)[0]

		first.dependency_add(lib)
		revisions = PackageRevision.objects.filter(package__slug=self.addon.slug)
		self.assertEqual(2, len(list(revisions)))

		first = PackageRevision.objects.filter(package__slug=self.addon.slug)[1]
		second = PackageRevision.objects.filter(package__slug=self.addon.slug)[0]

		self.assertEqual(0, len(first.dependencies.all()))
		self.assertEqual(1, len(second.dependencies.all()))

		second.dependency_remove(lib)

		first = PackageRevision.objects.filter(package__slug=self.addon.slug)[2]
		second = PackageRevision.objects.filter(package__slug=self.addon.slug)[1]
		third = PackageRevision.objects.filter(package__slug=self.addon.slug)[0]

		self.assertEqual(0, len(first.dependencies.all()))
		self.assertEqual(1, len(second.dependencies.all()))
		self.assertEqual(0, len(third.dependencies.all()))
		

	def test_adding_attachment(self):
		first = PackageRevision.objects.filter(package__slug=self.addon.slug)[0]
		first.attachment_create(
			filename=TEST_FILENAME,
			ext=TEST_FILENAME_EXTENSION,
			author=self.user
		)

		first = PackageRevision.objects.filter(package__slug=self.addon.slug)[1]
		second = PackageRevision.objects.filter(package__slug=self.addon.slug)[0]
		
		self.assertEqual(0, len(first.attachments.all()))
		self.assertEqual(1, len(second.attachments.all()))


	def test_adding_module(self):
		first = PackageRevision.objects.filter(package__slug=self.addon.slug)[0]
		first.module_create(
			filename=TEST_FILENAME,
			author=self.user
		)

		first = PackageRevision.objects.filter(package__slug=self.addon.slug)[1]
		second = PackageRevision.objects.filter(package__slug=self.addon.slug)[0]
		
		self.assertEqual(0, len(first.modules.all()))
		self.assertEqual(1, len(second.modules.all()))

