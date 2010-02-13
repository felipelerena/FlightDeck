from django.db.models.signals import pre_save, post_save
from django.db import models
from django.contrib.auth.models import User

from jetpack import settings

PERMISSION_CHOICE = {
	0: 'denied',
	1: 'view',
	2: 'full'
}

PERMISSION_CHOICES = []
for key,value in PERMISSION_CHOICE.items():
	PERMISSION_CHOICES.append((key,value))

STATUS_CHOICE = {
	'a': 'alpha',
	'b': 'beta',
	'p': 'production'
}
STATUS_CHOICES = []
for key,value in STATUS_CHOICE.items():
	STATUS_CHOICES.append((key,value))


class Cap(models.Model):
	slug = models.CharField(max_length=255, blank=True, unique=True, primary_key=True)
	name = models.CharField(max_length=255, unique=True)
	description = models.TextField(blank=True, null=True)

	author = models.ForeignKey(User, related_name="authored_capabilities")
	managers = models.ManyToManyField(User, related_name="managed_capabilities", blank=True)
	developers = models.ManyToManyField(User, related_name="developed_capabilities", blank=True)

	public_permission = models.IntegerField(choices=PERMISSION_CHOICES, default=2, blank=True)
	group_permission  = models.IntegerField(choices=PERMISSION_CHOICES, default=2, blank=True)
	
	def set_slug(self):
		self.slug = self.get_slug()

	def get_slug(self):
		from django.template.defaultfilters import slugify
		return slugify(self.name)

	@models.permalink
	def get_absolute_url(self):
		return ('capability_edit_base',[self.slug])

	@property
	def base_version(self):
		try:
			return CapVersion.objects.get(capability__slug=self.slug, is_base=True)
		except: 
			return None

	@property
	def public_permission_name(self):
		return PERMISSION_CHOICE[self.public_permission]

	@property
	def group_permission_name(self):
		return PERMISSION_CHOICE[self.group_permission]





class CapVersion(models.Model):
	capability = models.ForeignKey(Cap, related_name='versions')

	name = models.CharField(max_length=255, default='0.0', blank=True)
	counter = models.IntegerField(blank=True)
	content = models.TextField(blank=True)
	description = models.TextField(blank=True, null=True)

	capabilities = models.ManyToManyField('CapVersion', blank=True, null=True)

	author = models.ForeignKey(User, related_name="capability_versions")
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='a', blank=True) 
	is_base = models.BooleanField(default=False, blank=True)

	
	class Meta:
		unique_together = ('capability', 'name', 'counter')

	def __unicode__(self):
		return "%s %s" % (self.jetpack.name, self.fullname)

	@models.permalink
	def get_absolute_url(self):
		return ('capability_edit_version',[self.capability.slug, self.name, self.counter])

	@property
	def fullname(self):
		return "%s.%d" % (self.name, self.counter)

	@property
	def status_name(self):
		return STATUS_CHOICE[self.status]



class Jet(models.Model):
	slug = models.CharField(max_length=255, blank=True, unique=True, primary_key=True)
	name = models.CharField(max_length=255, unique=True)
	description = models.TextField(blank=True, null=True)
	
	author = models.ForeignKey(User, related_name="authored_jetpacks")
	managers = models.ManyToManyField(User, related_name="managed_jetpacks", blank=True)
	developers = models.ManyToManyField(User, related_name="developed_jetpacks", blank=True)

	public_permission = models.IntegerField(choices=PERMISSION_CHOICES, default=2, blank=True)
	group_permission  = models.IntegerField(choices=PERMISSION_CHOICES, default=2, blank=True)

	def __unicode__(self):
		return self.name


	@models.permalink
	def get_absolute_url(self):
		return ('jetpack_edit_base',[self.slug])


	def set_slug(self):
		self.slug = self.get_slug()

	def get_slug(self):
		from django.template.defaultfilters import slugify
		return slugify(self.name)


	@property
	def base_version(self):
		try:
			return JetVersion.objects.get(jetpack__slug=self.slug, is_base=True)
		except: 
			return None

	@property
	def public_permission_name(self):
		return PERMISSION_CHOICE[self.public_permission]

	@property
	def group_permission_name(self):
		return PERMISSION_CHOICE[self.group_permission]



class JetVersion(models.Model):
	jetpack = models.ForeignKey(Jet, related_name="versions")

	author = models.ForeignKey(User, related_name="jetpack_versions")

	name = models.CharField(max_length=255, default='0.0', blank=True)
	counter = models.IntegerField(blank=True)
	manifest = models.TextField(blank=True, null=True)
	content = models.TextField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)

	capabilities = models.ManyToManyField(CapVersion, blank=True, null=True)

	status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='a', blank=True) 
	published = models.BooleanField(default=False, blank=True)
	is_base = models.BooleanField(default=False, blank=True)

	
	class Meta:
		unique_together = ('jetpack', 'name', 'counter')

	def __unicode__(self):
		return "%s %s" % (self.jetpack.name, self.fullname)

	@models.permalink
	def get_absolute_url(self):
		return ('jetpack_edit_version',[self.jetpack.slug, self.name, self.counter])

	@property
	def fullname(self):
		return "%s.%d" % (self.name, self.counter)

	@property
	def status_name(self):
		return STATUS_CHOICE[self.status]

########################################################################################
## Catching Signals

def make_slug_on_create(instance, **kwargs):
	if kwargs.get('raw',False): return
	if not instance.slug:
		instance.set_slug()
pre_save.connect(make_slug_on_create, sender=Cap)
pre_save.connect(make_slug_on_create, sender=Jet)


def increase_cap_version_counter(instance, **kwargs):
	if kwargs.get('raw', False): return
	# only if save as new version
	if kwargs.get('id', False): return 
	if instance.counter >= 0: return
	try:
		highest = CapVersion.objects.filter(
				capability__slug=instance.capability.slug, name=instance.name
			).order_by('-counter')[0].counter
		instance.counter = highest + 1
	except:
		instance.counter = 0
pre_save.connect(increase_cap_version_counter, sender=CapVersion)
	

def increase_jet_version_counter(instance, **kwargs):
	if kwargs.get('raw', False): return
	# only if save as new version
	if kwargs.get('id', False): return 
	if instance.counter >= 0: return
	try:
		highest = JetVersion.objects.filter(
				jetpack__slug=instance.jetpack.slug, name=instance.name
			).order_by('-counter')[0].counter
		instance.counter = highest + 1
	except:
		instance.counter = 0
pre_save.connect(increase_jet_version_counter, sender=JetVersion)


def first_jetpack_is_base(instance, **kwargs):
	"""
	There is always a base version
	"""
	if kwargs.get('raw', False): return
	if not instance.is_base:
		try:
			base_version = JetVersion.objects.get(jetpack__slug=instance.jetpack.slug, is_base=True)
			return
		except:
			instance.is_base = True
pre_save.connect(first_jetpack_is_base, sender=JetVersion)


def first_capability_is_base(instance, **kwargs):
	"""
	There is always a base version
	"""
	if kwargs.get('raw', False): return
	if not instance.is_base:
		try:
			base_version = CapVersion.objects.get(capability__slug=instance.capability.slug, is_base=True)
			return
		except:
			instance.is_base = True
pre_save.connect(first_capability_is_base, sender=CapVersion)

"""
This is not used and probably will never be
def new_is_base(instance, **kwargs):
	" Depending on settings new option has to be a base one one automatically "
	if kwargs.get('raw', False): return
	if instance.is_base: return
	if not settings.JETPACK_NEW_IS_BASE: return
	# TODO: something is bad here
	instance.is_base = True
pre_save.connect(new_is_base, sender=JetVersion)
"""	

def unbase_other_base_jetpack_version(instance, **kwargs):
	"""
	There may be only one base version
	"""
	if kwargs.get('raw', False): return
	if instance.is_base:
		try:
			base_versions = JetVersion.objects.filter(jetpack__slug=instance.jetpack.slug, is_base=True)
		except:
			return
		for base_version in base_versions:
			try:
				if instance.id and  base_version.id == instance.id: return
				base_version.is_base = False
				base_version.save()
			except:
				return
pre_save.connect(unbase_other_base_jetpack_version, sender=JetVersion)


def unbase_other_base_capability_version(instance, **kwargs):
	"""
	There may be only one base version
	"""
	if kwargs.get('raw', False): return
	if instance.is_base:
		try:
			base_versions = CapVersion.objects.filter(capability__slug=instance.capability.slug, is_base=True)
		except:
			return
		for base_version in base_versions:
			try:
				if instance.id and  base_version.id == instance.id: return
				base_version.is_base = False
				base_version.save()
			except:
				return
pre_save.connect(unbase_other_base_capability_version, sender=CapVersion)


