from django.db import models

class CapVersionManager(models.Manager):
	def get_base(self, slug):
		try:
			return self.get(capability__slug=slug, is_base=True)
		except:
			return None

class JetVersionManager(models.Manager):
	def get_base(self, slug):
		try:
			return self.get(jetpack__slug=slug, is_base=True)
		except:
			return None

