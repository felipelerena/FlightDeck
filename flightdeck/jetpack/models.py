import os
import csv
import shutil

from copy import deepcopy
from exceptions import TypeError

from django.db.models.signals import pre_save, post_save
from django.db import models
from django.utils import simplejson
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from jetpack import settings
from jetpack.managers import PackageManager
from jetpack.errors import 	SelfDependencyException, FilenameExistException, \
							UpdateDeniedException, AddingModuleDenied, AddingAttachmentDenied
from jetpack.xpi_utils import sdk_copy, xpi_build, xpi_remove 


PERMISSION_CHOICES = (
	(0, 'private'),
	(1, 'view'),
	(2, 'do not copy'),
	(3, 'edit')
)
TYPE_CHOICES = (
	('l', 'Library'), 
	('a', 'Add-on')
)


class Package(models.Model):
	"""
	Holds the meta data shared across all PackageRevisions
	"""
	# identification
	# it can be the same as database id, but if we want to copy the database 
	# some day or change to a document-oriented database it would be bad 
	# to have this relied on any database model
	id_number = models.CharField(max_length=255, unique=True, blank=True)

	# name of the Package
	full_name = models.CharField(max_length=255)
	# made from the full_name 
	# it is used to create Package directory for export
	name = models.CharField(max_length=255, blank=True)
	description = models.TextField(blank=True)

	# type - determining ability to specific options
	type = models.CharField(max_length=30, choices=TYPE_CHOICES)
	
	# author is the first person who created the Package
	author = models.ForeignKey(User, related_name='packages_originated')
	
	# is the Package visible for public?
	public_permission = models.IntegerField(
									choices=PERMISSION_CHOICES, 
									default=1, blank=True)

	# url for the Manifest
	url = models.URLField(verify_exists=False, blank=True, default='')

	# license on which this package is rekeased to the public
	license = models.CharField(max_length=255, blank=True, default='')

	# where to export modules
	lib_dir = models.CharField(max_length=100, blank=True, null=True)

	# this is set in the PackageRevision.set_version
	version_name = models.CharField(max_length=250, blank=True, null=True, 
									default=settings.INITIAL_VERSION_NAME)

	version = models.ForeignKey('PackageRevision', blank=True, null=True, related_name='package_deprecated')
	latest = models.ForeignKey('PackageRevision', blank=True, null=True, related_name='package_deprecated2')

	private_key = models.TextField(blank=True, null=True)
	public_key = models.TextField(blank=True, null=True)
	jid = models.CharField(max_length=255, blank=True, null=True)
	program_id = models.CharField(max_length=255, blank=True, null=True)

	created_at = models.DateTimeField(auto_now_add=True)
	last_update = models.DateTimeField(auto_now=True)

	class Meta: 
		ordering = ('-last_update','-created_at')

	objects = PackageManager()

	##################
	# Methods

	def __unicode__(self):
		return '%s v. %s by %s' % (self.full_name, self.version_name, self.author)

	def get_absolute_url(self):
		return reverse('jp_%s_details' % self.get_type_name(),
						args=[self.id_number])

	def get_latest_url(self):
		return reverse('jp_%s_latest' % self.get_type_name(),
						args=[self.id_number])

	def get_edit_latest_url(self):
		return reverse('jp_%s_edit_latest' % self.get_type_name(),
						args=[self.id_number])



	def is_addon(self):
		return self.type == 'a'

	def is_library(self):
		return self.type == 'l'

	def get_type_name(self):
		return settings.PACKAGE_SINGULAR_NAMES[self.type]

	def get_lib_dir(self):
		return self.lib_dir or settings.DEFAULT_LIB_DIR

	def get_data_dir(self):
		return settings.DEFAULT_DATA_DIR

	def get_unique_package_name(self):
		return "%s-%s" % (self.name, self.id_number)

	def set_name(self):
		self.name = self.make_name()

	def make_name(self):
		return slugify(self.full_name)
	
	def create_id_number(self):
		""" 
		get the highest id number and increment it
		"""
		all_packages = Package.objects.all().order_by('-id_number')
		return str(int(all_packages[0].id_number) + 1) if all_packages else str(settings.MINIMUM_PACKAGE_ID)

	def generate_key(self):
		"""
		create keypair, program_id and jid
		"""
		from ecdsa import SigningKey, NIST256p
		from cuddlefish.preflight import vk_to_jid, jid_to_programid, my_b32encode

		sk = SigningKey.generate(curve=NIST256p)
		sk_text = "private-jid0-%s" % my_b32encode(sk.to_string())
		vk = sk.get_verifying_key()
		vk_text = "public-jid0-%s" % my_b32encode(vk.to_string())
		self.jid = vk_to_jid(vk)
		self.program_id = jid_to_programid(self.jid)
		self.private_key = sk_text
		self.public_key = vk_text

	def make_dir(self, packages_dir):
		"""
		create package directories inside packages
		return package directory name
		"""
		package_dir = '%s/%s' % (packages_dir, self.get_unique_package_name())
		os.mkdir(package_dir)
		os.mkdir('%s/%s' % (package_dir, self.get_lib_dir()))
		if not os.path.isdir('%s/%s' % (package_dir, self.get_data_dir())):
			os.mkdir('%s/%s' % (package_dir, self.get_data_dir()))
		return package_dir

	def get_copied_full_name(self):
		full_name = self.full_name
		if not full_name.startswith('Copy of'):
			full_name = "Copy of %s" % full_name
		return full_name
		
	
	def copy(self, author):
		"""
		create copy of the package
		"""
		new_p = Package(
			full_name=self.get_copied_full_name(),
			description=self.description,
			type=self.type,
			author=author,
			public_permission=self.public_permission,
			url=self.url,
			license=self.license,
			lib_dir=self.lib_dir
		)
		new_p.save()
		return new_p
		


class PackageRevision(models.Model):
	"""
	contains data which may be changed and rolled back
	"""
	package = models.ForeignKey(Package, related_name='revisions')
	# public version name 
	# this is a tag used to mark important revisions
	version_name = models.CharField(max_length=250, blank=True, null=True, 
									default=settings.INITIAL_VERSION_NAME)
	# this makes the revision unique across the same package/user
	revision_number = models.IntegerField(blank=True, default=0)
	# commit message
	message = models.TextField(blank=True)

	# Libraries on which current package depends
	dependencies = models.ManyToManyField('self', blank=True, null=True, 
											symmetrical=False)

	# from which revision this mutation was originated
	origin = models.ForeignKey('PackageRevision', related_name='mutations', 
								blank=True, null=True)

	# person who owns this revision
	author = models.ForeignKey(User, related_name='package_revisions')

	created_at = models.DateTimeField(auto_now_add=True)

	#contributors for Manifest
	contributors = models.CharField(max_length=255, blank=True, default='')

	# main for the Manifest
	module_main = models.CharField(max_length=100, blank=True, default='main')
	

	class Meta: 
		ordering = ('-revision_number',)
		unique_together = ('package', 'author', 'revision_number')

	def __unicode__(self):
		version = 'v. %s ' % self.version_name if self.version_name else ''
		return '%s - %s %sr. %d by %s' % (
									settings.PACKAGE_SINGULAR_NAMES[self.package.type],
									self.package.full_name, version, 
									self.revision_number, self.author.get_profile()
									)

	def get_absolute_url(self):
		if self.version_name:
			if self.package.version.revision_number == self.revision_number:
				return self.package.get_absolute_url()
			return reverse(
				'jp_%s_version_details' % settings.PACKAGE_SINGULAR_NAMES[self.package.type], 
				args=[self.package.id_number, self.version_name])
		return reverse(
			'jp_%s_revision_details' % settings.PACKAGE_SINGULAR_NAMES[self.package.type], 
			args=[self.package.id_number, self.revision_number])


	def get_edit_url(self):
		return reverse(
			'jp_%s_revision_edit' % self.package.get_type_name(), 
			args=[self.package.id_number, self.revision_number])

	def get_save_url(self):
		return reverse(
			'jp_%s_revision_save' % self.package.get_type_name(), 
			args=[self.package.id_number, self.revision_number])

	def get_add_module_url(self):
		return reverse(
			'jp_%s_revision_add_module' % self.package.get_type_name(), 
			args=[self.package.id_number, self.revision_number])

	def get_remove_module_url(self):
		return reverse(
			'jp_%s_revision_remove_module' % self.package.get_type_name(), 
			args=[self.package.id_number, self.revision_number])

	def get_add_attachment_url(self):
		return reverse(
			'jp_%s_revision_add_attachment' % self.package.get_type_name(), 
			args=[self.package.id_number, self.revision_number])

	def get_remove_attachment_url(self):
		return reverse(
			'jp_%s_revision_remove_attachment' % self.package.get_type_name(), 
			args=[self.package.id_number, self.revision_number])

	def get_assign_library_url(self):
		return reverse(
			'jp_%s_revision_assign_library' % self.package.get_type_name(), 
			args=[self.package.id_number, self.revision_number])

	def get_remove_library_url(self):
		return reverse(
			'jp_%s_revision_remove_library' % self.package.get_type_name(), 
			args=[self.package.id_number, self.revision_number])



	def get_test_xpi_url(self):
		if self.package.type != 'a': 
			raise Exception('XPI might be created only from an Add-on')
		return reverse(	
			'jp_addon_revision_test', args=[self.package.id_number, self.revision_number])


	def get_download_xpi_url(self):
		if self.package.type != 'a': 
			raise Exception('XPI might be created only from an Add-on')
		return reverse(	
			'jp_addon_revision_xpi', args=[self.package.id_number, self.revision_number])

	def get_copy_url(self):
		return reverse(
			'jp_%s_revision_copy' % self.package.get_type_name(), 
			args=[self.package.id_number, self.revision_number])

	


	######################
	# Manifest

	def get_contributors_list(self):
		csv_r = csv.reader([self.contributors], skipinitialspace=True)
		for c in csv_r:
			return c

	def get_dependencies_list(self):
		deps = ['jetpack-core']
		deps.extend([dep.package.get_unique_package_name() for dep in self.dependencies.all()])
		return deps

	def get_full_description(self):
		" return joined description "
		description = self.package.description
		if self.message:
			description = "%s\n%s" % (description, self.message)
		return description
		
	def get_full_rendered_description(self):
		" return description prepared for rendering "
		return "<p>%s</p>" % self.get_full_description().replace("\n","<br/>")

	def get_manifest(self, test_in_browser=False):
		if self.version_name:
			version = self.version_name
		else:
			version = "%s rev. %d" % (self.package.version_name, self.revision_number)

		if test_in_browser: 
			version = "%s - test" % version

		name = self.package.name if self.package.is_addon() else self.package.get_unique_package_name()
		manifest = {
			'fullName': self.package.full_name,
			'name': name,
			'description': self.get_full_description(),
			'author': self.package.author.username,
			'id': self.package.jid if self.package.is_addon() else self.package.id_number,
			'version': version,
			'dependencies': self.get_dependencies_list(),
			'license': self.package.license,
			'url': str(self.package.url),
			'contributors': self.get_contributors_list(),
			'lib': self.package.get_lib_dir()
		}
		if self.package.is_addon():
			manifest['main'] = self.module_main
			
		return manifest

	def get_manifest_json(self, **kwargs):
		return simplejson.dumps(self.get_manifest(**kwargs))


	def get_main_module(self):
		" return executable Module for Add-ons "
		if type == 'l': return None

		# find main module
		main = self.modules.filter(filename=self.module_main)
		if not main:
			raise Exception('Every Add-on needs to be linked with an executable Module')
		return main[0]

	######################
	# revision save methods

	def save(self, **kwargs):
		"""
		overloading save is needed to prevent from updating the same revision
		use super(PackageRevision, self).save(**kwargs) if needed
		"""
		if self.id:
			# create new revision
			return self.save_new_revision(**kwargs)
		return super(PackageRevision, self).save(**kwargs)

	
	def save_new_revision(self, package=None, **kwargs):
		" save self as new revision with link to the origin. "
		origin = deepcopy(self)
		if package:
			self.package = package
			self.author = package.author
		self.id = None
		self.version_name = None
		self.origin = origin
		self.revision_number = self.get_next_revision_number()

		save_return = super(PackageRevision, self).save(**kwargs)
		# reassign all dependencies
		for dep in origin.dependencies.all():
			self.dependencies.add(dep)

		for mod in origin.modules.all():
			self.modules.add(mod)

		for att in origin.attachments.all():
			self.attachments.add(att)

		self.package.latest = self
		self.package.save()
		if package:
			self.set_version('copy')
		return save_return


	def get_next_revision_number(self):
		""" 
		find latest revision_number for the self.package and self.user
		@return latest revisiion number or 1
		"""
		revision_numbers = PackageRevision.objects.filter(
									author__username=self.author.username,
									package__id_number=self.package.id_number
								).order_by('-revision_number')
		return revision_numbers[0].revision_number + 1 if revision_numbers else 1

	
	def set_version(self, version_name, current=True):
		"""
		@param String version_name: name of the version
		@param Boolean current: should the version become a current one
		@returns result of save revision

		Set the version_name
		update the PackageRevision obeying the overload save
		Set current Package:version_name and Package:version if current
		"""
		# check if there isn't a version with such a name
		revisions = PackageRevision.objects.filter(package__pk=self.package.pk)
		for revision in revisions:
			if revision.version_name == version_name:
				version_name = ''
				#raise Exception("There is already a revision with that name")
		self.version_name = version_name
		if current:
			self.package.version_name = version_name
			self.package.version = self
			self.package.save()

		return super(PackageRevision, self).save()

	def validate_module_filename(self, filename):
		for mod in self.modules.all():
			if mod.filename == filename:
				return False
		return True

	def validate_attachment_filename(self, filename, ext):
		for mod in self.attachments.all():
			if mod.filename == filename and mod.ext == ext:
				return False
		return True

	def module_create(self, **kwargs):
		" create module and add to modules "
		# validate if given filename is valid
		if not self.validate_module_filename(kwargs['filename']):
			raise FilenameExistException(
				'Sorry, there is already a module in your add-on with the name "%s". Each module in your add-on needs to have a unique name.' % kwargs['filename']
			)
		mod = Module.objects.create(**kwargs)
		self.module_add(mod)
		return mod

	def module_add(self, mod):
		" copy to new revision, add module "
		# save as new version
		# validate if given filename is valid
		if not self.validate_module_filename(mod.filename):
			raise FilenameExistException(
				'Sorry, there is already a module in your add-on with the name "%s". Each module in your add-on needs to have a unique name.' % mod.filename
			)
		"""
		I think it's not necessary
		TODO: check integration
		for rev in mod.revisions.all():
			if rev.package.id_number != self.package.id_number:
				raise AddingModuleDenied('this module is already assigned to other Library - %s' % rev.package.get_unique_package_name())
		"""
		self.save()
		return self.modules.add(mod)

		
	def module_remove(self, mod):
		" copy to new revision, remove module "
		# save as new version
		self.save()
		return self.modules.remove(mod)
		
	def module_update(self, mod):
		" to update a module, new package revision has to be created "
		self.save()
		self.modules.remove(mod)
		mod.id = None
		mod.save()
		self.modules.add(mod)


	def modules_update(self, modules):
		" update more than one module "
		self.save()
		for mod in modules:
			self.modules.remove(mod)
			mod.id = None
			mod.save()
			self.modules.add(mod)


	def attachment_create(self, **kwargs):
		" create attachment and add to attachments "
		# validate if given filename is valid
		if not self.validate_attachment_filename(kwargs['filename'], kwargs['ext']):
			raise FilenameExistException(
				'Sorry, there is already an attachment in your add-on with the name "%s.%s". Each attachment in your add-on needs to have a unique name.' % (
					kwargs['filename'], kwargs['ext']
				)
			)
		att = Attachment.objects.create(**kwargs)
		self.attachment_add(att)
		return att


	def attachment_add(self, att):
		" copy to new revision, add attachment "
		# save as new version
		# validate if given filename is valid
		if not self.validate_attachment_filename(att.filename, att.ext):
			raise FilenameExistException(
				'Attachment with filename %s.%s already exists' % (att.filename, att.ext)
			)
		"""
		for rev in att.revisions.all():
			if rev.package.id_number != self.package.id_number:
				raise AddingAttachmentDenied('this attachment is already assigned to other Library - %s' % rev.package.get_unique_package_name())
		"""
		self.save()
		return self.attachments.add(att)
		
	def attachment_remove(self, dep):
		" copy to new revision, remove attachment "
		# save as new version
		self.save()
		return self.attachments.remove(dep)
		

	def dependency_add(self, dep):
		" copy to new revision, add dependency (existing Library - PackageVersion) "
		# a PackageRevision has to depend on the LibraryRevision only
		if dep.package.type != 'l': 
			raise TypeError('Dependency has to be a Library')
		# a LibraryRevision can't depend on another LibraryRevision linked with the same
		# Library
		if dep.package.id_number == self.package.id_number:
			raise SelfDependencyException('A Library can not depend on itself!')
		# dependency have to be unique in the PackageRevision
		deps = self.dependencies.all()
		for d in deps:
			if d.package.pk == dep.package.pk:
				raise Exception('Your add-on is already using "%s" by %s.' % (dep.package.full_name, dep.package.author.get_profile()));
		# save as new version
		self.save()
		return self.dependencies.add(dep)
		
	def dependency_remove(self, dep):
		" copy to new revision, remove dependency "
		# save as new version
		self.save()
		return self.dependencies.remove(dep)


	def dependency_remove_by_id_number(self, id_number):
		" find dependency by its id_number call dependency_remove "
		for dep in self.dependencies.all():
			if dep.package.id_number == id_number:
				self.dependency_remove(dep)
				return True
		raise Exception('There is no such library in this %s' % self.package.get_type_name())

	def get_dependencies_list_json(self):
		l = [{
				'full_name': d.package.full_name, 
				'view_url': d.get_absolute_url(),
				'edit_url': d.get_edit_url()
				} for d in self.dependencies.all()
			] if len(self.dependencies.all()) > 0 else []
		return simplejson.dumps(l)
		
	def get_modules_list_json(self):
		l = [{
				'filename': m.filename,
				'author': m.author.username,
				'executable': self.module_main == m.filename
				} for m in self.modules.all()
			] if len(self.modules.all()) > 0 else []
		return simplejson.dumps(l)


	def get_sdk_name(self):
		return '%s-%s' % (self.package.id_number, self.revision_number)

	
	def get_sdk_dir(self):
		return '%s-%s' % (settings.SDKDIR_PREFIX, self.get_sdk_name())


	def build_xpi(self):
		" prepare and build XPI "
		if self.package.type == 'l':
			raise Exception('only Add-ons may build a XPI')

		sdk_dir = self.get_sdk_dir()
		# TODO: consider SDK staying per PackageRevision...
		if os.path.isdir(sdk_dir):
			xpi_remove(sdk_dir)
		sdk_copy(sdk_dir)
		self.export_keys(sdk_dir)
		self.export_files_with_dependencies('%s/packages' % sdk_dir)
		return (xpi_build(sdk_dir, 
				'%s/packages/%s' % (sdk_dir, self.package.get_unique_package_name()))
				)

	def build_xpi_test(self, modules):
		" prepare and build XPI for test only (unsaved modules) "
		if self.package.type == 'l':
			raise Exception('only Add-ons may build a XPI')

		sdk_dir = self.get_sdk_dir()
		# TODO: consider SDK staying per PackageRevision...
		if os.path.isdir(sdk_dir):
			xpi_remove(sdk_dir)
		sdk_copy(sdk_dir)
		self.export_keys(sdk_dir)

		packages_dir = '%s/packages' % sdk_dir
		package_dir = self.package.make_dir(packages_dir)
		self.export_manifest(package_dir)
		# instead of export modules
		lib_dir = '%s/%s' % (package_dir, self.package.get_lib_dir())
		for mod in self.modules.all():
			mod_edited = False
			for e_mod in modules:
				if e_mod.pk == mod.pk:
					mod_edited = True
					e_mod.export_code(lib_dir)
			if not mod_edited:
				mod.export_code(lib_dir)
		self.export_attachments('%s/%s' % (package_dir, self.package.get_data_dir()))
		self.export_dependencies(packages_dir)
		return (xpi_build(sdk_dir, 
				'%s/packages/%s' % (sdk_dir, self.package.get_unique_package_name()))
				)


	def export_keys(self, sdk_dir):
		" export private and public keys "
		keydir = '%s/%s' % (sdk_dir, settings.KEYDIR)
		if not os.path.isdir(keydir):
			os.mkdir(keydir)
		handle = open('%s/%s' % (keydir, self.package.jid), 'w')
		handle.write('private-key:%s\n' % self.package.private_key)
		handle.write('public-key:%s' % self.package.public_key)
		handle.close()



	def export_manifest(self, package_dir):
		handle = open('%s/package.json' % package_dir, 'w')
		handle.write(self.get_manifest_json())
		handle.close()
		

	def export_modules(self, lib_dir):
		for mod in self.modules.all():
			mod.export_code(lib_dir)


	def export_attachments(self, static_dir):
		for att in self.attachments.all():
			att.export_file(static_dir)


	def export_dependencies(self, packages_dir):
		for lib in self.dependencies.all():
			lib.export_files_with_dependencies(packages_dir)

	def export_files(self, packages_dir):
		package_dir = self.package.make_dir(packages_dir)
		self.export_manifest(package_dir)
		self.export_modules('%s/%s' % (package_dir, self.package.get_lib_dir()))
		self.export_attachments('%s/%s' % (package_dir, self.package.get_data_dir()))

	def export_files_with_dependencies(self, packages_dir):
		self.export_files(packages_dir)
		self.export_dependencies(packages_dir)


	def get_version_name(self): 
		name = '%s ' % self.version_name if self.version_name else ''
		return '%srev. %s' % (name, self.revision_number)

class Module(models.Model):
	" the only way to 'change' the module is to assign it to different PackageRequest "
	revisions = models.ManyToManyField(PackageRevision, 
									related_name='modules', blank=True)
	# name of the Module - it will be used as javascript file name
	filename = models.CharField(max_length=255)
	# Code of the module
	code = models.TextField(blank=True)
	# user who has written current revision of the module
	author = models.ForeignKey(User, related_name='module_revisions')

	class Meta:
		ordering = ('filename',)


	def __unicode__(self):
		return '%s by %s (%s)' % (self.get_filename(), self.author, self.get_package_fullName())

	def get_package(self):
		try:
			return self.revisions.all()[0].package
		except:
			return None

	def get_package_fullName(self):
		package = self.get_package()
		return package.full_name if package else ''

	def get_filename(self):
		return "%s.js" % self.filename

	def save(self, **kwargs):
		if self.id:
			raise UpdateDeniedException('Module can not be updated in the same row')
		return super(Module, self).save(**kwargs)

	def export_code(self, lib_dir):
		handle = open('%s/%s.js' % (lib_dir, self.filename), 'w')
		handle.write(self.code)
		handle.close()
		



class Attachment(models.Model):
	
	revisions = models.ManyToManyField(PackageRevision, 
									related_name='attachments', blank=True)
	# filename of the attachment
	filename = models.CharField(max_length=255)
	# extension name
	ext = models.CharField(max_length=10)

	# upload path
	path = models.CharField(max_length=255)

	# user who has uploaded the file
	author = models.ForeignKey(User, related_name='attachments')
	# mime will help with displaying the attachment
	mimetype = models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		ordering = ('filename',)

	def get_filename(self):
		name = self.filename
		if self.ext:
			name = "%s.%s" % (name, self.ext)
		return name

	def save(self, **kwargs):
		if self.id:
			raise UpdateDeniedException('Attachment can not be updated in the same row')
		return super(Attachment, self).save(**kwargs)

	def export_file(self, static_dir):
		shutil.copy('%s/%s' % (settings.UPLOAD_DIR, self.path), 
					'%s/%s.%s' % (static_dir, self.filename, self.ext))

	def get_display_url(self):
		return reverse('jp_attachment', args=[self.path])



#################################################################################
## Catching Signals

def set_package_id_number(instance, **kwargs):
	if kwargs.get('raw', False): return
	if instance.id: return
	instance.id_number = instance.create_id_number()
pre_save.connect(set_package_id_number, sender=Package)


def make_name(instance, **kwargs):
	if kwargs.get('raw',False): return
	if not instance.name:
		instance.set_name()
pre_save.connect(make_name, sender=Package)

def make_keypair_on_create(instance, **kwargs):
	if kwargs.get('raw',False): return
	if instance.id: return
	if instance.is_addon():
		instance.generate_key()
pre_save.connect(make_keypair_on_create, sender=Package)



def save_first_revision(instance, **kwargs):
	"""
	Create first PackageRevision
	"""
	if kwargs.get('raw', False): return
	# only for the new Package
	if not kwargs.get('created', False): return

	revision = PackageRevision(package=instance, author=instance.author)
	revision.save()
	instance.version = revision
	instance.latest = revision
	if instance.is_addon():
		mod = Module.objects.create(
			filename=revision.module_main,
			author=instance.author,
			code="""// This is an active module of the %s Add-on
exports.main = function() {};""" % instance.full_name
		)
		revision.modules.add(mod)
	instance.save()

post_save.connect(save_first_revision, sender=Package)

