# Taken from feincms
# http://github.com/matthiask/feincms/blob/master/feincms/__init__.py

# Do not use Django settings at module level as recommended
from django.utils.functional import LazyObject
 
class LazySettings(LazyObject):
	def _setup(self):
		from amo import default_settings
		self._wrapped = Settings(default_settings)
 
class Settings(object):
	def __init__(self, settings_module):
		for setting in dir(settings_module):
			if setting == setting.upper():
				setattr(self, setting, getattr(settings_module, setting))
 
settings = LazySettings()


