import os
import shutil
import subprocess
from copy import deepcopy
from exceptions import TypeError

from django.test import TestCase
from django.utils import simplejson
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from test_utils import create_test_user
from jetpack.models import Package, PackageRevision, Module, Attachment
from jetpack import settings
from jetpack.errors import 	SelfDependencyException, FilenameExistException, \
							UpdateDeniedException, AddingModuleDenied, AddingAttachmentDenied
from jetpack.xpi_utils import sdk_copy, xpi_build, xpi_remove

TEST_USERNAME = 'test_user'
TEST_ADDON_FULLNAME = 'test Addon'
TEST_ADDON_NAME = 'test-addon'
TEST_LIBRARY_FULLNAME = 'test Library'
TEST_LIBRARY_NAME = 'test-library'
TEST_ADDON2_FULLNAME = 'test Addon 2'
TEST_FILENAME = 'file-name'
TEST_FILENAME_EXTENSION = 'css'
TEST_UPLOAD_PATH = 'test/abc'
SDKDIR = '/tmp/test-SDK'

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

		test_dirs = ['%s/test' % settings.UPLOAD_DIR, SDKDIR]
		for test_dir in test_dirs:
			if os.path.isdir(test_dir):
				shutil.rmtree(test_dir)

	def mkUploadDir(self):
		os.mkdir('%s/test' % settings.UPLOAD_DIR)
	
	def createFile(self):
		self.mkUploadDir()
		handle = open('%s/%s' % (settings.UPLOAD_DIR, TEST_UPLOAD_PATH), 'w')
		handle.write('test uploaded file')
		handle.close()



class PackageTest(PackageTestCase):
	# self user, addon, library are created

	def test_addon_creation(self):
		addon = Package.objects.get(full_name=TEST_ADDON_FULLNAME)
		self.failUnless(addon)
		self.assertEqual(addon.id_number, str(settings.MINIMUM_PACKAGE_ID))
		self.failUnless(addon.version)
		self.failUnless(addon.latest)


	def test_library_creation(self):
		library = Package.objects.get(full_name=TEST_LIBRARY_FULLNAME)
		self.failUnless(library)
		self.assertEqual(library.id_number, str(settings.MINIMUM_PACKAGE_ID + 1))
		self.failUnless(library.version)
		self.failUnless(library.latest)


	def test_name_creation(self):
		self.assertEqual(self.addon.name, TEST_ADDON_NAME)
		self.assertEqual(self.library.name, TEST_LIBRARY_NAME)


	def test_ordering(self):
		"""
		Newest is first
		"""
		addon2 = Package(full_name=TEST_ADDON2_FULLNAME, author=self.user, type='a')
		addon2.save()
		self.to_delete.append(addon2)
		self.assertEqual(Package.objects.all()[0].full_name, TEST_ADDON2_FULLNAME)
		

	def test_filtering(self):
		addon2 = Package(full_name=TEST_ADDON2_FULLNAME, author=self.user, type='a')
		addon2.save()
		self.to_delete.append(addon2)

		self.assertEqual(len(list((Package.objects.addons()))), 2)
		self.assertEqual(len(list((Package.objects.libraries()))), 1)


	def test_related_name(self):
		self.assertEqual(len(list(self.user.packages_originated.all())), 2)


	def test_directory_name(self):
		self.assertEqual(
			self.addon.get_unique_package_name(),
			"%s-%d" % (TEST_ADDON_NAME, settings.MINIMUM_PACKAGE_ID)
		)


class PackageRevisionTest(PackageTestCase):

	def test_first_revision(self):
		revisions = PackageRevision.objects.filter(package__name=self.addon.name)
		self.assertEqual(1, len(list(revisions)))
		revision = revisions[0]
		self.assertEqual(revision.author.username, self.addon.author.username)
		self.assertEqual(revision.revision_number, 0)

	
	def test_save(self):
		# system should create new revision on save
		revisions = PackageRevision.objects.filter(package__name=self.addon.name)
		first = revisions[0]
		first.save()
		revisions = PackageRevision.objects.filter(package__name=self.addon.name)
		self.assertEqual(2, len(list(revisions)))
		self.assertEqual(None, first.version_name)
		addon = Package.objects.get(pk=self.addon.pk)
		self.assertEqual(addon.latest.revision_number, first.revision_number)
		self.assertNotEqual(addon.version.revision_number, addon.latest.revision_number)


	def test_set_version(self):
		revisions = PackageRevision.objects.filter(package__name=self.addon.name)
		first = revisions[0]
		old_id = first.id
		first.set_version('test')
		# setting version does not make new revision
		self.assertEqual(first.id, old_id)
		# setting version sets it for revision, package and assigns revision to package
		self.assertEqual(first.version_name,'test')
		self.assertEqual(first.package.version_name,'test')
		self.assertEqual(first.package.version.pk, first.pk)
		
	def test_absolute_urls(self):
		revisions = PackageRevision.objects.filter(package__name=self.addon.name)
		p_rev = revisions[0]
		self.assertEqual(
			reverse('jp_addon_details', args=[self.addon.id_number]),
			p_rev.get_absolute_url())

		p_rev.set_version('test')
		self.assertEqual(
			reverse('jp_addon_details', args=[self.addon.id_number]),
			p_rev.get_absolute_url())

		p_rev.save()
		# p_rev needs to be reloaded as package.version points to an instance
		revisions = PackageRevision.objects.filter(package__name=self.addon.name)
		p_rev = revisions[0]
		self.assertEqual(
			reverse('jp_addon_revision_details', 
					args=[self.addon.id_number, p_rev.revision_number]),
			p_rev.get_absolute_url())

		p_rev.set_version('test2', False)
		self.assertEqual(
			reverse('jp_addon_version_details', args=[self.addon.id_number, 'test2']),
			p_rev.get_absolute_url())
		
	
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
			path=TEST_UPLOAD_PATH,
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


	def test_updating_module(self):
		
		first = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		mod = first.module_create(
			filename=TEST_FILENAME,
			author=self.user
		)
		mod.code = 'test'
		first.module_update(mod)

		self.assertEqual(3, len(PackageRevision.objects.filter(package__name=self.addon.name)))
		self.assertEqual(2, len(Module.objects.filter(filename=TEST_FILENAME)))

		first = PackageRevision.objects.filter(package__name=self.addon.name)[1]
		last = PackageRevision.objects.filter(package__name=self.addon.name)[0]

		self.assertEqual(2,len(last.modules.all()))
		
		


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
		
	def test_adding_attachment_which_was_added_to_other_package_before(self):
		" assigning attachment to more than one packages should be prevented! "
		addon = Package.objects.create(
			full_name="Other Package", 
			author=self.user, 
			type='a'
		)
		rev = PackageRevision.objects.filter(package__name='other-package')[0]
		first = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		att = Attachment.objects.create(
			filename=TEST_FILENAME,
			ext=TEST_FILENAME_EXTENSION,
			path=TEST_UPLOAD_PATH,
			author=self.user
		)
		first.attachment_add(att)
		self.assertRaises(AddingAttachmentDenied, rev.attachment_add, att)
		

	def test_adding_attachment_with_existing_filename(self):
		
		first = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		first.attachment_create(
			filename=TEST_FILENAME,
			ext=TEST_FILENAME_EXTENSION,
			path=TEST_UPLOAD_PATH,
			author=self.user
		)
		self.assertRaises(FilenameExistException, first.attachment_create,
			**{	'filename': TEST_FILENAME,
				'ext': TEST_FILENAME_EXTENSION,
				'author': self.user,
				'path': TEST_UPLOAD_PATH,
				}
		)

		att = Attachment.objects.create(
			filename=TEST_FILENAME,
			ext=TEST_FILENAME_EXTENSION,
			path=TEST_UPLOAD_PATH,
			author=self.user
		)
		self.assertRaises(FilenameExistException, first.attachment_add, att)



class ModuleTest(PackageTestCase):

	def test_update_module_using_save(self):
		" updating module is not allowed "
		mod = Module.objects.create(
			filename=TEST_FILENAME,
			author=self.user
		)
		self.assertRaises(UpdateDeniedException,mod.save)


class AttachmentTest(PackageTestCase):

	def setUp(self):
		super(AttachmentTest, self).setUp()
		self.attachment = Attachment.objects.create(
			filename=TEST_FILENAME,
			ext=TEST_FILENAME_EXTENSION,
			path=TEST_UPLOAD_PATH,
			author=self.user
		)
		

	def test_update_attachment_using_save(self):
		" updating attachment is not allowed "
		self.assertRaises(UpdateDeniedException,self.attachment.save)

	def test_export_file(self):
		self.createFile()
		self.attachment.export_file('/tmp')
		self.failUnless(os.path.isfile('/tmp/%s.%s' % (TEST_FILENAME, TEST_FILENAME_EXTENSION)))

		
class ManifestsTest(PackageTestCase):
	" tests strictly about manifest creation "

	manifest = {
		'fullName': TEST_ADDON_FULLNAME,
		'name': TEST_ADDON_NAME,
		'description': '',
		'author': TEST_USERNAME,
		'version': settings.INITIAL_VERSION_NAME,
		'dependencies': ['jetpack-core'],
		'license': '',
		'url': '',
		'main': 'main',
		'contributors': [],
		'lib': 'lib'
	}
	
	def test_minimal_manifest(self):
		" test if self.manifest is created for the clean addon "
		first = PackageRevision.objects.filter(package__name=self.addon.name)[0]

		manifest = deepcopy(self.manifest)
		first_manifest = first.get_manifest()
		del first_manifest['id']
		self.assertEqual(manifest, first_manifest)


	def test_manifest_from_not_current_revision(self):
		" test if the version in the manifest changes after 'updating' PackageRevision "
		first = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		first.save()

		manifest = deepcopy(self.manifest)
		manifest['version'] = "%s rev. 1" % settings.INITIAL_VERSION_NAME

		first_manifest = first.get_manifest()
		del first_manifest['id']
		self.assertEqual(manifest, first_manifest)


	def test_manifest_with_dependency(self):
		" test if Manifest has the right dependency list "
		first = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		lib = PackageRevision.objects.filter(package__name=self.library.name)[0]
		first.dependency_add(lib)

		manifest = deepcopy(self.manifest)
		manifest['dependencies'].append('%s-%d' % (TEST_LIBRARY_NAME, settings.MINIMUM_PACKAGE_ID + 1))
		manifest['version'] = "%s rev. 1" % settings.INITIAL_VERSION_NAME

		first_manifest = first.get_manifest()
		del first_manifest['id']
		self.assertEqual(manifest, first_manifest)

	def test_contributors_list(self):
		" test if the contributors list is exported properly "
		first = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		first.contributors = "one, 12345, two words,no space"
		first.save()

		manifest = deepcopy(self.manifest)
		manifest['version'] = "%s rev. 1" % settings.INITIAL_VERSION_NAME
		manifest['contributors'] = ['one', '12345', 'two words', 'no space']

		first_manifest = first.get_manifest()
		del first_manifest['id']
		self.assertEqual(manifest, first_manifest)
		

class XPIBuildTest(PackageTest):
	"""
	Test if the stuff is properly build
	"""

	def makeSDKDir(self):
		os.mkdir (SDKDIR) 
		os.mkdir('%s/packages' % SDKDIR)

	def setUp(self):
		super (XPIBuildTest, self).setUp()
		self.addonrev = PackageRevision.objects.filter(package__name=self.addon.name)[0]
		self.librev = PackageRevision.objects.filter(package__name=self.library.name)[0]
		self.librev.module_create(
			filename=TEST_FILENAME,
			author=self.user)


	def test_package_dir_generation(self):
		" test if all package dirs are created properly "
		self.makeSDKDir()
		package_dir = self.library.make_dir('%s/packages' % SDKDIR)
		self.failUnless(os.path.isdir(package_dir))
		self.failUnless(os.path.isdir('%s/%s' % (package_dir, self.library.get_lib_dir())))
		

	def test_save_modules(self):
		" test if module is saved "
		self.makeSDKDir()
		package_dir = self.library.make_dir('%s/packages' % SDKDIR)
		self.librev.export_modules('%s/%s' % (package_dir, self.library.get_lib_dir()))

		self.failUnless(os.path.isfile('%s/packages/%s/%s/%s.js' % (
							SDKDIR, 
							self.library.get_unique_package_name(), 
							self.library.get_lib_dir(),
							TEST_FILENAME)))
		
	def test_manifest_file_creation(self):
		" test if manifest is created properly "
		self.makeSDKDir()
		package_dir = self.library.make_dir('%s/packages' % SDKDIR)
		self.librev.export_manifest(package_dir)
		self.failUnless(os.path.isfile('%s/package.json' % package_dir))
		handle = open('%s/package.json' % package_dir)
		manifest_json = handle.read()
		manifest = simplejson.loads(manifest_json)
		self.assertEqual(manifest, self.librev.get_manifest())

		
	def test_minimal_lib_export(self):
		" test if all the files are in place "
		self.makeSDKDir()
		self.librev.export_files_with_dependencies('%s/packages' % SDKDIR)
		package_dir = '%s/packages/%s' % (SDKDIR, self.library.get_unique_package_name())
		self.failUnless(os.path.isdir(package_dir))
		self.failUnless(os.path.isdir('%s/%s' % (package_dir, self.library.get_lib_dir())))
		self.failUnless(os.path.isfile('%s/package.json' % package_dir))
		self.failUnless(os.path.isfile('%s/%s/%s.js' % (
							package_dir, 
							self.library.get_lib_dir(),
							TEST_FILENAME)))


	def test_addon_export_with_dependency(self):
		" test if lib and main.js are properly exported "
		self.makeSDKDir()
		addon_dir = '%s/packages/%s' % (SDKDIR, self.addon.get_unique_package_name())
		lib_dir = '%s/packages/%s' % (SDKDIR, self.library.get_unique_package_name())

		self.addonrev.dependency_add(self.librev)
		self.addonrev.export_files_with_dependencies('%s/packages' % SDKDIR)
		self.failUnless(os.path.isdir('%s/%s' % (addon_dir, self.addon.get_lib_dir())))
		self.failUnless(os.path.isdir('%s/%s' % (lib_dir, self.library.get_lib_dir())))
		self.failUnless(os.path.isfile('%s/%s/%s.js' % (
							addon_dir, 
							self.addon.get_lib_dir(),
							self.addonrev.module_main)))
		

	def test_addon_export_with_attachment(self):
		" test if attachment file is coped "
		self.makeSDKDir()
		self.createFile()
		addon_dir = '%s/packages/%s' % (SDKDIR, self.addon.get_unique_package_name())
		self.addonrev.attachment_create(
			filename=TEST_FILENAME,
			ext=TEST_FILENAME_EXTENSION,
			path=TEST_UPLOAD_PATH,
			author=self.user
		)
		self.addonrev.export_files_with_dependencies('%s/packages' % SDKDIR)
		self.failUnless(os.path.isfile('%s/%s/%s.%s' % (
							addon_dir,
							self.addon.get_data_dir(),
							TEST_FILENAME, TEST_FILENAME_EXTENSION)))


	def test_copying_sdk(self):
		sdk_copy(SDKDIR)
		self.failUnless(os.path.isdir(SDKDIR))


	def test_minimal_xpi_creation(self):
		" xpi build from an addon straight after creation "
		sdk_copy(SDKDIR)
		self.addonrev.export_files_with_dependencies('%s/packages' % SDKDIR)
		out = xpi_build(SDKDIR, 
					'%s/packages/%s' % (SDKDIR, self.addon.get_unique_package_name()))
		# assert no error output
		self.assertEqual('', out[1])
		# assert xpi was created
		self.failUnless(os.path.isfile('%s/packages/%s/%s.xpi' % (
			SDKDIR, self.addon.get_unique_package_name(), self.addon.name)))

	def test_addon_with_other_modules(self):
		" addon has now more modules "
		self.addonrev.module_create(
			filename=TEST_FILENAME,
			author=self.user
		)
		sdk_copy(SDKDIR)
		self.addonrev.export_files_with_dependencies('%s/packages' % SDKDIR)
		out = xpi_build(SDKDIR, 
					'%s/packages/%s' % (SDKDIR, self.addon.get_unique_package_name()))
		# assert no error output
		self.assertEqual('', out[1])
		self.failUnless(out[0])
		# assert xpi was created
		self.failUnless(os.path.isfile('%s/packages/%s/%s.xpi' % (
			SDKDIR, self.addon.get_unique_package_name(), self.addon.name)))


	def test_xpi_with_empty_dependency(self):
		" empty lib is created "
		lib = Package.objects.create(
			full_name=TEST_LIBRARY_FULLNAME, 
			author=self.user, 
			type='l'
		)
		librev = PackageRevision.objects.filter(package__id_number=lib.id_number)[0]
		self.addonrev.dependency_add(librev)
		sdk_copy(SDKDIR)
		self.addonrev.export_files_with_dependencies('%s/packages' % SDKDIR)
		out = xpi_build(SDKDIR, 
					'%s/packages/%s' % (SDKDIR, self.addon.get_unique_package_name()))
		# assert no error output
		self.assertEqual('', out[1])
		# assert xpi was created
		self.failUnless(os.path.isfile('%s/packages/%s/%s.xpi' % (
			SDKDIR, self.addon.get_unique_package_name(), self.addon.name)))


	def test_xpi_with_dependency(self):
		" addon has one dependency with a file "
		self.addonrev.dependency_add(self.librev)
		sdk_copy(SDKDIR)
		self.addonrev.export_files_with_dependencies('%s/packages' % SDKDIR)
		out = xpi_build(SDKDIR, 
					'%s/packages/%s' % (SDKDIR, self.addon.get_unique_package_name()))
		# assert no error output
		self.assertEqual('', out[1])
		# assert xpi was created
		self.failUnless(os.path.isfile('%s/packages/%s/%s.xpi' % (
			SDKDIR, self.addon.get_unique_package_name(), self.addon.name)))
		

class ManyUsersTests(TestCase):
	
	fixtures = ['test_users.json', 'test_basic_usecase.json']

	def test_fixtures_loaded(self):
		self.failUnless(User.objects.get(username='1234567'))
		self.failUnless(Package.objects.all()[0])
