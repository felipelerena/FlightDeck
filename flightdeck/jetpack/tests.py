from copy import deepcopy
from exceptions import TypeError

from django.test import TestCase

from test_utils import create_test_user
from jetpack.models import Package, PackageRevision, Module, Attachment
from jetpack import settings
from jetpack.errors import 	SelfDependencyException, FilenameExistException, \
							UpdateDeniedException, AddingModuleDenied

TEST_USERNAME = 'test_user'
TEST_ADDON_FULLNAME = 'test Addon'
TEST_ADDON_NAME = 'test-addon'
TEST_LIBRARY_FULLNAME = 'test Library'
TEST_LIBRARY_NAME = 'test-library'
TEST_ADDON2_FULLNAME = 'test Addon 2'
TEST_FILENAME = 'file-name'
TEST_FILENAME_EXTENSION = 'css'

class PackageTestCase(TestCase):
	def setUp(self):
		self.to_delete = []
		self.user = create_test_user(username=TEST_USERNAME)
		self.addon = Package(
			full_name=TEST_ADDON_FULLNAME, 
			author=self.user, 
			type='a'
		)
		self.addon.save()
		self.to_delete.append(self.addon)
		self.library = Package(
			full_name=TEST_LIBRARY_FULLNAME, 
			author=self.user, 
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
		addon = Package.objects.get(full_name=TEST_ADDON_FULLNAME)
		self.failUnless(addon)
		self.assertEqual(addon.id_number, settings.MINIMUM_PACKAGE_ID)


	def test_library_creation(self):
		library = Package.objects.get(full_name=TEST_LIBRARY_FULLNAME)
		self.failUnless(library)
		self.assertEqual(library.id_number, settings.MINIMUM_PACKAGE_ID + 1)


	def test_name_creation(self):
		self.assertEqual(self.addon.name, TEST_ADDON_NAME)
		self.assertEqual(self.library.name, TEST_LIBRARY_NAME)


	def test_ordering(self):
		addon2 = Package(full_name=TEST_ADDON2_FULLNAME, author=self.user, type='a')
		addon2.save()
		self.to_delete.append(addon2)

		self.assertEqual(Package.objects.all()[0].full_name, TEST_ADDON2_FULLNAME)
		

	def test_filtering(self):
		addon2 = Package(full_name=TEST_ADDON2_FULLNAME, author=self.user, type='a')
		addon2.save()
		self.to_delete.append(addon2)

		self.assertEqual(len(list((Package.objects.addons().all()))), 2)
		self.assertEqual(len(list((Package.objects.libraries().all()))), 1)


	def test_related_name(self):
		self.assertEqual(len(list(self.user.packages_originated.all())), 2)


	def test_directory_name(self):
		self.assertEqual(
			self.addon.get_directory_name(),
			"%s-%d" % (TEST_ADDON_NAME, settings.MINIMUM_PACKAGE_ID)
		)


class PackageRevisionTest(PackageTestCase):

	def test_first_revision(self):
		revisions = PackageRevision.objects.filter(package__name=self.addon.name)
		self.assertEqual(1, len(list(revisions)))
		revision = revisions[0]
		self.assertEqual(revision.owner.username, self.addon.author.username)
		self.assertEqual(revision.revision_number, 0)

	
	def test_save(self):
		# system should create new revision on save
		revisions = PackageRevision.objects.filter(package__name=self.addon.name)
		first = revisions[0]
		first.save()
		revisions = PackageRevision.objects.filter(package__name=self.addon.name)
		self.assertEqual(2, len(list(revisions)))
		self.assertEqual(None, first.version_name)

	
	def test_save_with_dependency(self):
		# system should copy on save with all dependencies
		first = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		lib = PackageRevision.objects.filter(package__name=self.library.name)[0]
		first.dependencies.add(lib)
		first.save()

		first = PackageRevision.objects.filter(package__name=self.addon.name)[1]
		second = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		self.assertEqual(second.dependencies.all()[0].package.name, lib.package.name)
		self.assertEqual(
			first.dependencies.all()[0].package.name, 
			second.dependencies.all()[0].package.name
		)


	def test_adding_addon_as_dependency(self):
		lib = PackageRevision.objects.filter(package__name=self.library.name)[0]
		addon = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		self.assertRaises(TypeError, lib.dependency_add, addon)
		self.assertEqual(0, len(lib.dependencies.all()))


	def test_adding_library_to_itself_as_dependency(self):
		lib = PackageRevision.objects.filter(package__name=self.library.name)[0]
		self.assertRaises(SelfDependencyException, lib.dependency_add, lib)


	def test_adding_and_removing_dependency(self):
		first = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		lib = PackageRevision.objects.filter(package__name=self.library.name)[0]

		first.dependency_add(lib)
		revisions = PackageRevision.objects.filter(package__name=self.addon.name)
		self.assertEqual(2, len(list(revisions)))

		first = PackageRevision.objects.filter(package__name=self.addon.name)[1]
		second = PackageRevision.objects.filter(package__name=self.addon.name)[0]

		self.assertEqual(0, len(first.dependencies.all()))
		self.assertEqual(1, len(second.dependencies.all()))

		second.dependency_remove(lib)

		first = PackageRevision.objects.filter(package__name=self.addon.name)[2]
		second = PackageRevision.objects.filter(package__name=self.addon.name)[1]
		third = PackageRevision.objects.filter(package__name=self.addon.name)[0]

		self.assertEqual(0, len(first.dependencies.all()))
		self.assertEqual(1, len(second.dependencies.all()))
		self.assertEqual(0, len(third.dependencies.all()))
		

	def test_adding_attachment(self):
		first = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		first.attachment_create(
			filename=TEST_FILENAME,
			ext=TEST_FILENAME_EXTENSION,
			author=self.user
		)

		first = PackageRevision.objects.filter(package__name=self.addon.name)[1]
		second = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		
		self.assertEqual(0, len(first.attachments.all()))
		self.assertEqual(1, len(second.attachments.all()))


	def test_adding_module(self):
		first = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		first.module_create(
			filename=TEST_FILENAME,
			author=self.user
		)

		first = PackageRevision.objects.filter(package__name=self.addon.name)[1]
		second = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		
		self.assertEqual(1, len(first.modules.all()))
		self.assertEqual(2, len(second.modules.all()))


	def test_adding_module_which_was_added_to_other_package_before(self):
		" assigning module to more than one packages should be prevented! "
		addon = Package.objects.create(
			full_name="Other Package", 
			author=self.user, 
			type='a'
		)
		rev = PackageRevision.objects.filter(package__name='other-package')[0]
		first = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		mod = Module.objects.create(
			filename=TEST_FILENAME,
			author=self.user
		)
		first.module_add(mod)
		self.assertRaises(AddingModuleDenied, rev.module_add, mod)
		

	def test_adding_module_with_existing_filename(self):
		
		first = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		first.module_create(
			filename=TEST_FILENAME,
			author=self.user
		)
		self.assertRaises(FilenameExistException, first.module_create,
			**{'filename':TEST_FILENAME,'author':self.user}
		)
		mod = Module.objects.create(
			filename=TEST_FILENAME,
			author=self.user
		)
		self.assertRaises(FilenameExistException, first.module_add, mod)
		

	def test_adding_attachment_with_existing_filename(self):
		
		first = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		first.attachment_create(
			filename=TEST_FILENAME,
			ext=TEST_FILENAME_EXTENSION,
			author=self.user
		)
		self.assertRaises(FilenameExistException, first.attachment_create,
			**{'filename':TEST_FILENAME,'ext':TEST_FILENAME_EXTENSION,'author':self.user}
		)

		att = Attachment.objects.create(
			filename=TEST_FILENAME,
			ext=TEST_FILENAME_EXTENSION,
			author=self.user
		)
		self.assertRaises(FilenameExistException, first.attachment_add, att)



class ModuleTest(PackageTestCase):

	def test_update_module(self):
		" updating module is not allowed "
		mod = Module.objects.create(
			filename=TEST_FILENAME,
			author=self.user
		)
		self.assertRaises(UpdateDeniedException,mod.save)
		


class AttachmentTest(PackageTestCase):

	def test_update_attachment(self):
		" updating attachment is not allowed "
		att = Attachment.objects.create(
			filename=TEST_FILENAME,
			ext=TEST_FILENAME_EXTENSION,
			author=self.user
		)
		self.assertRaises(UpdateDeniedException,att.save)
		
class ManifestsTest(PackageTestCase):
	" tests strictly about manifest creation "

	manifest = {
		'fullName': TEST_ADDON_FULLNAME,
		'name': TEST_ADDON_NAME,
		'description': '',
		'author': TEST_USERNAME,
		'id': settings.MINIMUM_PACKAGE_ID,
		'version': settings.INITIAL_VERSION_NAME,
		'dependencies': [],
		'license': '',
		'url': '',
		'contributors': []
	}
	
	def test_minimal_manifest(self):
		" test if self.manifest is created for the clean addon "
		first = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		self.assertEqual(self.manifest, first.get_manifest())


	def test_manifest_tested(self):
		first = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		
		manifest = deepcopy(self.manifest)
		manifest['version'] = "%s - test" % settings.INITIAL_VERSION_NAME

		self.assertEqual(manifest, first.get_manifest(True))
		

	def test_mnifest_from_not_current_revision(self):
		" test if the version in the manifest changes after 'updating' PackageRevision "
		first = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		first.save()

		manifest = deepcopy(self.manifest)
		manifest['version'] = "%s rev. 1" % settings.INITIAL_VERSION_NAME

		self.assertEqual(manifest, first.get_manifest())


	def test_manifest_with_dependency(self):
		" test if Manifest has the right dependency list "
		first = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		lib = PackageRevision.objects.filter(package__name=self.library.name)[0]
		first.dependency_add(lib)

		manifest = deepcopy(self.manifest)
		manifest['dependencies'] = ['%s-%d' % (TEST_LIBRARY_NAME, settings.MINIMUM_PACKAGE_ID + 1)]
		manifest['version'] = "%s rev. 1" % settings.INITIAL_VERSION_NAME

		self.assertEqual(manifest, first.get_manifest())

	def test_contributors_list(self):
		" test if the contributors list is exported properly "
		first = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		first.contributors = "one, 12345, two words,no space"
		first.save()

		manifest = deepcopy(self.manifest)
		manifest['version'] = "%s rev. 1" % settings.INITIAL_VERSION_NAME
		manifest['contributors'] = ['one', '12345', 'two words', 'no space']

		self.assertEqual(manifest, first.get_manifest())
		

class XPIBuildTest(PackageTest):
	"""
	Test if the stuff is properly build
	"""
	def setUp(self):
		super (XPIBuildTest, self).setUp()
		self.addonrev = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		self.librev = PackageRevision.objects.filter(package__name=self.library.name)[0]
		self.librev.module_create(
			filename=TEST_FILENAME,
			author=self.user
		)

	def test_minimal_xpi_creation(self):
		" xpi build from an addon straight after creation "


	def test_addon_with_other_modules(self):
		" addon has now moremodules "


	def test_xpi_with_empty_dependency(self):
		" empty lib is created "

	def test_xpi_with_dependency(self):
		" addon has one dependency with a file "
		self.addonrev.dependency_add(self.librev)
		
