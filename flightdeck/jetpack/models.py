from django.db.models.signals import pre_save, post_save
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from jetpack import settings
from jetpack.managers import PackageManager

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
	# it can be the same as database id, but if we want to copy the database some day or change
	# to a document-oriented database it shouldn't rely on database model
	id_number = models.PositiveIntegerField(unique=True)

	# name of the Package
	name = models.CharField(max_length=255)
	# made from the name 
	# it is used to create a directory of Modules
	slug = models.CharField(max_length=255, blank=True)
	# description
	description = models.TextField(blank=True)

	# type - determining ability to specific options
	type = models.CharField(max_length=30, choices=TYPE_CHOICES)
	
	# creator is the first person who created the Package
	# TODO: consider ability to change this (UI)
	creator = models.ForeignKey(User, related_name='packages_originated')
	# group of users who have management rights
	# managers = models.ManyToManyField(User, related_name='packages_managed', blank=True)
	# developers is a collected group of all developers who participated in Package development
	# developers = models.ManyToManyField(User, related_name='packages_developed', blank=True)
	
	# is the Package visible for public?
	public_permission = models.IntegerField(choices=PERMISSION_CHOICES, default=1, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	last_update = models.DateTimeField(auto_now=True)

	class Meta: 
		ordering = ('-last_update',)

	objects = PackageManager()

	##################
	# Methods

	def __unicode__(self):
		return self.name

	def set_slug(self):
		self.slug = self.make_slug()

	def make_slug(self):
		return slugify(self.name)


class PackageRevision(models.Model):
	"""
	contains data which may be changed and rolled back
	"""
	package = models.ForeignKey(Package, related_name='revisions')
	# public version name 
	# this is a tag used to mark important revisions
	version_name = models.CharField(max_length=250, blank=True, default='initial')
	# this makes the revision unique across the same package/user
	revision_number = models.IntegerField(blank=True, default=0)
	# commit message
	message = models.TextField(blank=True)

	# Libraries on which current package depends
	libraries = models.ManyToManyField('self', blank=True, null=True, symmetrical=False)

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
	# revision save methoda

	def set_as_head(self):
		self.was_head = True
		self.save()
	
	# save as a copy of the object (new revision) 
	def save_revision(self, user):
		if self.id:
			origin = deepcopy(self)
			self.id = None
			self.origin = origin
			self.revision_number = self.get_next_revision_number()
		else:
			self.was_head = True

		self.owner = user
		self.save()

	def get_next_revision_number(self):
		# find latest revision_number for the self.package and self.user
		revision_numbers = PackageRevision.objects.filter(
									owner__username=self.owner.username,
									package__slug=self.package.slug
								).order_by('-revision_number')
		return revision_numbers[0].revision_number + 1 if revision_number else 1


class Module(models.Model):
	
	revision = models.ForeignKey(PackageRevision)
	# name of the Module - it will be used as javascript file name
	filename = models.CharField(max_length=255, unique=True)
	# Capability Content - main code of the Capability
	content = models.TextField(blank=True)
	# user who has written current revision of the module
	author = models.ForeignKey(User, related_name='module revisions')

	class Meta:
		unique_together = ('revision', 'filename')


########################################################################################
## Catching Signals

def make_slug_on_create(instance, **kwargs):
	if kwargs.get('raw',False): return
	if not instance.slug:
		instance.set_slug()
pre_save.connect(make_slug_on_create, sender=Package)


def save_first_revision(instance, **kwargs):
	"""
	Create first PackageRevision and set as head
	"""
	if kwargs.get('raw', False): return
	# only for the new Package
	if not kwargs.get('created', False): return

	revision = PackageRevision(package=instance)
	revision.save_revision(instance.creator)
	instance.set_head(revision)
post_save.connect(save_first_revision, sender=Package)

