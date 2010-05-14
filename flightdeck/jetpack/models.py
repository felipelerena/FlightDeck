from copy import deepcopy
from exceptions import TypeError

from django.db.models.signals import pre_save, post_save
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from jetpack import settings
from jetpack.managers import PackageManager
from jetpack.errors import SelfDependencyException

PERMISSION_CHOICES = (
	(0, 'private'),
	(1, 'view'),
	(2, 'edit')
)
TYPE_CHOICES = (
	('l', 'Library'), 
	('a', 'Addon')
)


class Package(models.Model):
	"""
	Holds the meta data shared across all PackageRevisions
	"""
	# identification
	# it can be the same as database id, but if we want to copy the database 
	# some day or change to a document-oriented database it would be bad 
	# to have this relied on any database model
	id_number = models.PositiveIntegerField(unique=True)

	# name of the Package
	name = models.CharField(max_length=255)
	# made from the name 
	# it is used to create a directory of Modules
	slug = models.CharField(max_length=255, blank=True)
	description = models.TextField(blank=True)

	# type - determining ability to specific options
	type = models.CharField(max_length=30, choices=TYPE_CHOICES)
	
	# creator is the first person who created the Package
	creator = models.ForeignKey(User, related_name='packages_originated')
	
	# is the Package visible for public?
	public_permission = models.IntegerField(
									choices=PERMISSION_CHOICES, 
									default=1, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	last_update = models.DateTimeField(auto_now=True)

	class Meta: 
		ordering = ('-last_update',)

	objects = PackageManager()

	##################
	# Methods

	def set_slug(self):
		self.slug = self.make_slug()

	def make_slug(self):
		return slugify(self.name)
	
	def get_next_id_number(self):
		""" 
		get the highest id number and increment it
		"""
		all_packages = Package.objects.all().order_by('-id_number')
		return all_packages[0].id_number + 1 if all_packages else settings.MINIMUM_PACKAGE_ID

	def get_directory_name(self):
		return "%s-%d" % (self.slug, self.id_number)



class PackageRevision(models.Model):
	"""
	contains data which may be changed and rolled back
	"""
	package = models.ForeignKey(Package, related_name='revisions')
	# public version name 
	# this is a tag used to mark important revisions
	version_name = models.CharField(max_length=250, blank=True, null=True, 
									default='initial')
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
	owner = models.ForeignKey(User, related_name='package_revisions')

	created_at = models.DateTimeField(auto_now_add=True)

	class Meta: 
		ordering = ('-revision_number',)
		unique_together = ('package', 'owner', 'revision_number')

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

	
	def save_new_revision(self, **kwargs):
		" save self as new revision with link to the origin. "
		origin = deepcopy(self)
		self.id = None
		self.origin = origin
		self.revision_number = self.get_next_revision_number()
		# a hook for future "branching"
		if kwargs.has_key('user'):
			self.owner = kwargs['user']
			del kwargs['user']

		save_return = super(PackageRevision, self).save(**kwargs)
		# reassign all dependencies
		for dep in origin.dependencies.all():
			self.dependencies.add(dep)

		for mod in origin.modules.all():
			self.modules.add(mod)

		for att in origin.attachments.all():
			self.attachments.add(att)

		return save_return


	def get_next_revision_number(self):
		""" 
		find latest revision_number for the self.package and self.user
		@return latest revisiion number or 1
		"""
		revision_numbers = PackageRevision.objects.filter(
									owner__username=self.owner.username,
									package__id_number=self.package.id_number
								).order_by('-revision_number')
		return revision_numbers[0].revision_number + 1 if revision_numbers else 1

	
	def set_version(self, version):
		" Set the version and update the revision obeying the overload save "
		self.version = version
		return super(PackageRevision, self).save()

	def module_create(self, **kwargs):
		" create module and add to modules "
		mod = Module.objects.create(**kwargs)
		self.module_add(mod)

	def module_add(self, mod):
		" copy to new revision, add module "
		# save as new version
		self.save()
		return self.modules.add(mod)
		
	def module_remove(self, dep):
		" copy to new revision, remove module "
		# save as new version
		self.save()
		return self.modules.remove(dep)
		

	def attachment_create(self, **kwargs):
		" create attachment and add to attachments "
		mod = Attachment.objects.create(**kwargs)
		self.attachment_add(mod)

	def attachment_add(self, att):
		" copy to new revision, add attachment "
		# save as new version
		self.save()
		return self.attachments.add(att)
		
	def attachment_remove(self, dep):
		" copy to new revision, remove attachment "
		# save as new version
		self.save()
		return self.attachments.remove(dep)
		

	def dependency_add(self, dep):
		" copy to new revision, add dependency (Library - PackageVersion) "
		# a PackageRevision has to depend on the LibraryRevision only
		if dep.package.type != 'l': 
			raise TypeError('Dependency has to be a Library')
		# a LibraryRevision can't depend on another LibraryRevision linked with the same
		# Library
		if dep.package.id_number == self.package.id_number:
			raise SelfDependencyException('A Library can not depend on itself!')
		# save as new version
		self.save()
		return self.dependencies.add(dep)
		
	def dependency_remove(self, dep):
		" copy to new revision, remove dependency "
		# save as new version
		self.save()
		return self.dependencies.remove(dep)
		


class Module(models.Model):
	
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

	def get_filename(self):
		return "%s.js" % self.filename



class Attachment(models.Model):
	
	revisions = models.ManyToManyField(PackageRevision, 
									related_name='attachments', blank=True)
	# path to the attachment
	filename = models.CharField(max_length=255)
	# extension name
	ext = models.CharField(max_length=10)
	# user who has uploaded the file
	author = models.ForeignKey(User, related_name='attachments')
	# mime will help with displaying the attachment
	mimetype = models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		ordering = ('filename',)

	def get_filename(self):
		return "%s.%s" % (self.filename, self.ext)


#################################################################################
## Catching Signals

def set_package_id_number(instance, **kwargs):
	if kwargs.get('raw', False): return
	if instance.id: return
	instance.id_number = instance.get_next_id_number()
pre_save.connect(set_package_id_number, sender=Package)


def make_slug_on_create(instance, **kwargs):
	if kwargs.get('raw',False): return
	if not instance.slug:
		instance.set_slug()
pre_save.connect(make_slug_on_create, sender=Package)


def save_first_revision(instance, **kwargs):
	"""
	Create first PackageRevision
	"""
	if kwargs.get('raw', False): return
	# only for the new Package
	if not kwargs.get('created', False): return

	revision = PackageRevision(package=instance, owner=instance.creator)
	revision.save()
post_save.connect(save_first_revision, sender=Package)

