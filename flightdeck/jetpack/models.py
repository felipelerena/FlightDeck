from django.db.models.signals import pre_save, post_save
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from jetpack import settings
from jetpack.managers import JetVersionManager, CapVersionManager

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
	"""
	Representation of Capability metadata in the database
	"""
	# name of the Capability - it will be used in manifest
	name = models.CharField(max_length=255, unique=True)
	# unified id made from the name used to identify Capability data in the database
	slug = models.CharField(max_length=255, blank=True, unique=True, primary_key=True)
	# description of the Capability itself - high level
	description = models.TextField(blank=True, null=True)

	# Creator of the Capability - the person who created the Jetpack
	creator = models.ForeignKey(User, related_name="authored_capabilities")
	# group of people who may change Capability identity (Cap data)
	managers = models.ManyToManyField(User, related_name="managed_capabilities", blank=True)
	# users to whom the group permission applies
	developers = models.ManyToManyField(User, related_name="developed_capabilities", blank=True)

	# permission applied to all FlightDeck users
	public_permission = models.IntegerField(choices=PERMISSION_CHOICES, default=2, blank=True)
	# permission applied to all developers
	group_permission  = models.IntegerField(choices=PERMISSION_CHOICES, default=2, blank=True)

	added_at = models.DateTimeField(auto_now_add=True) 
	last_update = models.DateTimeField(auto_now=True) 

	class Meta:
		ordering = ('-last_update',)
	
	###################
	# Properties

	type = "capability"

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

	##################
	# Methods

	def __unicode__(self):
		return self.name

	def set_slug(self):
		self.slug = self.get_slug()

	def get_slug(self):
		from django.template.defaultfilters import slugify
		return slugify(self.name)

	@models.permalink
	def get_absolute_url(self):
		return ('jp_capability_edit',[self.slug])

	@models.permalink
	def get_update_url(self):
		return ('jp_capability_update',[self.slug])

	@models.permalink
	def get_version_create_url(self):
		return ('jp_capability_version_create',[self.slug])

	@models.permalink
	def get_versions_url(self):
		return reverse("jp_capability_get_versions", args=[self.slug])


	@staticmethod
	def get_create_url():
		"""
		@returns str: create new jetpack url
		"""
		return reverse('jp_capability_create')

	def can_be_updated_by(self, user):
		"""
		Can user save Capability's metadata
		@returns boolean: 
		"""
		return (self.creator.username == user.username or user in self.managers.all())


class CapVersion(models.Model):
	"""
	Version of the Cap - it defines Capability entity (together with the Cap)
	"""
	# which Capability is this version assigned to
	capability = models.ForeignKey(Cap, related_name='versions')

	# who authored this particular version (same as creator if first version)
	author = models.ForeignKey(User, related_name="capability_versions")

	# Name of the version - it will be extended with the counter in fullname property
	name = models.CharField(max_length=255, default='0.0', blank=True)
	# version counter - automatically changed value (set in signals)
	counter = models.IntegerField(blank=True)
	# Capability Content - main code of the Capability
	content = models.TextField(blank=True)
	# This version only description
	description = models.TextField(blank=True, null=True)

	# List of CapVersions this CapVersion relies on
	capabilities = models.ManyToManyField('CapVersion', blank=True, null=True)

	# alpha/beta/production
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='a', blank=True) 
	# is this version the base one for the Capability
	is_base = models.BooleanField(default=False, blank=True)

	added_at = models.DateTimeField(auto_now_add=True) 
	last_update = models.DateTimeField(auto_now=True) #

	objects = CapVersionManager()
	
	class Meta:
		# there may be only one version with the same name and counter for the Capability
		unique_together = ('capability', 'name', 'counter')
		ordering = ('-name','-counter')


	###################
	# Properties

	@property
	def fullname(self):
		"""
		@returns str: full version number (name and counter after a dot)
		"""
		return "%s.%d" % (self.name, self.counter)

	@property
	def listname(self):
		return self.capability.name

	@property
	def slug(self):
		return self.capability.slug

	@property
	def status_name(self):
		return STATUS_CHOICE[self.status]


	##################
	# Methods

	def __unicode__(self):
		"""
		@returns str: jetpack name and its full version number
		"""
		return "%s %s" % (self.capability.name, self.fullname)

	@models.permalink
	def get_absolute_url(self):
		"""
		@returns str: url to the edit page of this version
		"""
		return ('jp_capability_version_edit',[self.capability.slug, self.name, self.counter])

	@models.permalink
	def get_update_url(self):
		"""
		@returns str: url to update the same version (no url changed afterwards)
		"""
		return ('jp_capability_version_update',[self.capability.slug, self.name, self.counter])

	@models.permalink
	def get_set_as_base_url(self):
		"""
		@returns str: url to switch the is_base to True
		"""
		return ('jp_capability_version_save_as_base',[self.capability.slug, self.name, self.counter])

	@models.permalink
	def get_adddependency_url(self):
		return ('jp_capability_add_dependency',[self.capability.slug, self.name, self.counter])



class Jet(models.Model):
	"""
	Representation of Jetpack metadata in the database
	"""
	# name of the Jetpack - it will be used in manifest
	name = models.CharField(max_length=255, unique=True)
	# unified name used to identify Jetpack data in the database
	slug = models.CharField(max_length=255, blank=True, unique=True, primary_key=True)
	# description of the Jetpack itself - high level
	description = models.TextField(blank=True, null=True)
	
	# Creator of the Jetpack - the person who created the Jetpack
	creator = models.ForeignKey(User, related_name="authored_jetpacks")
	# group of people who may change Jetpack identity (Jet data)
	managers = models.ManyToManyField(User, related_name="managed_jetpacks", blank=True)
	# users to whom the group permission applies
	developers = models.ManyToManyField(User, related_name="developed_jetpacks", blank=True)

	# permission applied to all FlightDeck users
	public_permission = models.IntegerField(choices=PERMISSION_CHOICES, default=2, blank=True)
	# permission applied to all developers
	group_permission  = models.IntegerField(choices=PERMISSION_CHOICES, default=2, blank=True)

	added_at = models.DateTimeField(auto_now_add=True) 
	last_update = models.DateTimeField(auto_now=True) 

	class Meta:
		ordering = ('-last_update',)

	###################
	# Properties

	type = "jetpack"

	@property
	def base_version(self):
		"""
		Get the only Version which is base (there may be only one)
		"""
		return JetVersion.objects.get_base(self.slug)			

	@property
	def public_permission_name(self):
		return PERMISSION_CHOICE[self.public_permission]

	@property
	def group_permission_name(self):
		return PERMISSION_CHOICE[self.group_permission]

	##################
	# Methods
	
	def __unicode__(self):
		return self.name

	def set_slug(self):
		self.slug = self.get_slug()


	def get_slug(self):
		"""
		@returns str: slugified the name
		"""
		from django.template.defaultfilters import slugify
		return slugify(self.name)


	@models.permalink
	def get_absolute_url(self):
		return ('jp_jetpack_edit',[self.slug])


	@models.permalink
	def get_update_url(self):
		return ('jp_jetpack_update',[self.slug])


	@models.permalink
	def get_version_create_url(self):
		return ('jp_jetpack_version_create',[self.slug])


	def can_be_updated_by(self, user):
		"""
		Can user save Jetpack's metadata
		@returns boolean: 
		"""
		return (self.creator.username == user.username or user in self.managers.all())

	def get_versions_url(self):
		return reverse("jp_jetpack_get_versions", args=[self.slug])

	@staticmethod
	def get_create_url():
		"""
		@returns str: create new jetpack url
		"""
		return reverse('jp_jetpack_create')




class JetVersion(models.Model):
	"""
	Version of the Jet - it defines Jetpack entity (together with the Jet)
	"""
	# which jetpack is this version assigned to
	jetpack = models.ForeignKey(Jet, related_name="versions")

	# who authored this particular version (same as creator if first version)
	author = models.ForeignKey(User, related_name="jetpack_versions")

	# Name of the version - it will be extended with the counter in fullname property
	name = models.CharField(max_length=255, default='0.0', blank=True)
	# version counter - automatically changed value (set in signals)
	counter = models.IntegerField(blank=True)
	# Jetpack Manifest - JSON object defining Jetpack metadata and assigned capabilities
	manifest = models.TextField(blank=True, null=True)
	# Jetpack Content - main code of the Jetpack
	content = models.TextField(blank=True, null=True)
	# This version only description
	description = models.TextField(blank=True, null=True)

	# List of CapVersions this JetVersion relies on
	capabilities = models.ManyToManyField(CapVersion, blank=True, null=True)

	# alpha/beta/production
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='a', blank=True) 
	# is the Jetpack published to AMO with this version
	published = models.BooleanField(default=False, blank=True)
	# is this version the base one for the Jetpack
	is_base = models.BooleanField(default=False, blank=True)

	added_at = models.DateTimeField(auto_now_add=True) 
	last_update = models.DateTimeField(auto_now=True) 

	objects = JetVersionManager()
	
	class Meta:
		# there may be only one version with the same name and counter for the Jetpack
		unique_together = ('jetpack', 'name', 'counter')
		ordering = ('-name','-counter')


	###################
	# Properties

	@property
	def fullname(self):
		"""
		@returns str: full version number (name and counter after a dot)
		"""
		return "%s.%d" % (self.name, self.counter)

	@property
	def listname(self):
		return self.jetpack.name

	@property
	def slug(self):
		return self.jetpack.slug

	@property
	def status_name(self):
		return STATUS_CHOICE[self.status]

	##################
	# Methods

	def __unicode__(self):
		"""
		@returns str: jetpack name and its full version number
		"""
		return "%s %s" % (self.jetpack.name, self.fullname)

	@models.permalink
	def get_absolute_url(self):
		"""
		@returns str: url to the edit page of this version
		"""
		return ('jp_jetpack_version_edit',[self.jetpack.slug, self.name, self.counter])

	@models.permalink
	def get_update_url(self):
		"""
		@returns str: url to update the same version (no url changed afterwards)
		"""
		return ('jp_jetpack_version_update',[self.jetpack.slug, self.name, self.counter])

	@models.permalink
	def get_set_as_base_url(self):
		"""
		@returns str: url to switch the is_base to True
		"""
		return ('jp_jetpack_version_save_as_base',[self.jetpack.slug, self.name, self.counter])


	@models.permalink
	def get_adddependency_url(self):
		return ('jp_jetpack_add_dependency',[self.jetpack.slug, self.name, self.counter])


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


