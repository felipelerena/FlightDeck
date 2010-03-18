from django.db import models

class CapVersionManager(models.Manager):
	def get_base(self, slug):
		try:
			return self.select_related().get(capability__slug=slug, is_base=True)
		except:
			return None

	def filter_by_slug(self, slug):
		 return self.select_related().filter(capability__slug=slug)


class JetVersionManager(models.Manager):
	def get_base(self, slug):
		try:
			return self.select_related().get(jetpack__slug=slug, is_base=True)
		except:
			return None

	def filter_by_slug(self, slug):
		 return self.select_related().filter(jetpack__slug=slug)

