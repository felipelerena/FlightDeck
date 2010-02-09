from django.db.models.signals import pre_save, post_save

from jetpack import settings
from jetpack.models import Jetpack, Version


# ------------------------------------------
# Jetpack signals
		
def make_slug_on_create(instance, **kwargs):
	if kwargs.get('raw',False): return
	if not instance.id and not instance.slug:
		instance.set_slug()
pre_save.connect(make_slug_on_create, sender=Jetpack)

# ------------------------------------------
# Version signals

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


