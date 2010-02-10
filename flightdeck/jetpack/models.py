from django.db.models.signals import pre_save, post_save
from django.db import models
from django.contrib.auth.models import User

from jetpack import settings


class Jetpack(models.Model):
	PERMISSIONS_CHOICES = (
		(0, 'denied'),
		(1, 'view'),
		(2, 'edit'),
	)

	slug = models.CharField(max_length=20, blank=True)
	name = models.CharField(max_length=255)
	decription = models.TextField(blank=True, null=True)
	author = models.ForeignKey(User, related_name="authored_jetpacks")
	managers = models.ManyToManyField(User, related_name="managed_jetpacks", blank=True)
	developers = models.ManyToManyField(User, related_name="developed_jetpacks", blank=True)
	public_permission = models.IntegerField(choices=PERMISSIONS_CHOICES, default=2, blank=True)
	group_permission  = models.IntegerField(choices=PERMISSIONS_CHOICES, default=2, blank=True)


	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('jetpack_edit_base',[self.slug])

	def set_slug(self):
		from utils import random_string
		check_slug = True
		while check_slug:
			self.slug = random_string(settings.JETPACK_SLUG_LENGTH)
			try:
				Jetpack.objects.get(slug=self.slug)
			except:
				check_slug = False

	@property
	def base_version(self):
		try:
			return Version.objects.get(jetpack__id=self.id, is_base=True)
		except: 
			return None

		
def make_slug_on_create(instance, **kwargs):
	if kwargs.get('raw',False): return
	if not instance.id and not instance.slug:
		instance.set_slug()
pre_save.connect(make_slug_on_create, sender=Jetpack)



STATUS_CHOICES = (
	('a', 'alpha'),
	('b', 'beta'),
	('p', 'production')
)

class Version(models.Model):
	jetpack = models.ForeignKey(Jetpack, related_name="versions")
	commited_by = models.ForeignKey(User, related_name="commits")
	name = models.CharField(max_length=255, blank=True)
	decription = models.TextField(blank=True, null=True)
	code = models.TextField(blank=True, null=True)
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='a', blank=True) 
	published = models.BooleanField(default=False, blank=True)
	is_base = models.BooleanField(default=False, blank=True)

	def __unicode__(self):
		return "%s v%s" % (self.jetpack.name, self.name)

	@models.permalink
	def get_absolute_url(self):
		return ('jetpack_edit_version',[self.jetpack.slug, self.name])


def default_name(instance, **kwargs):
	"""
	If name not given set from Jetpack
	"""
	if kwargs.get('raw', False): return
	if not instance.name:
		instance.name = instance.jetpack.name
pre_save.connect(default_name, sender=Version)
	

def first_is_base(instance, **kwargs):
	"""
	There is always a base version
	"""
	if kwargs.get('raw', False): return
	if not instance.is_base:
		try:
			base_version = Version.objects.get(jetpack__id=instance.jetpack.id, is_base=True)
			return
		except:
			instance.is_base = True
pre_save.connect(first_is_base, sender=Version)


def new_is_base(instance, **kwargs):
	"""
	Depending on settings new option has to be a base one one automatically
	"""
	if kwargs.get('raw', False): return
	if instance.is_base: return
	if not settings.JETPACK_NEW_IS_BASE: return
	# TODO: something is bad here
	instance.is_base = True
pre_save.connect(new_is_base, sender=Version)
	

def unbase_other_base_version(instance, **kwargs):
	"""
	There may be only one base version
	"""
	if kwargs.get('raw', False): return
	if instance.is_base:
		try:
			base_versions = Version.objects.filter(jetpack__id=instance.jetpack.id, is_base=True)
		except:
			return
		for base_version in base_versions:
			try:
				if instance.id and  base_version.id == instance.id: return
				base_version.is_base = False
				base_version.save()
			except:
				return
pre_save.connect(unbase_other_base_version, sender=Version)


