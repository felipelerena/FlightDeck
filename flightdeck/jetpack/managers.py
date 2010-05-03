from django.db import models

class PackageManager(models.Manager):

	def addons(self):
		return self.filter(type="a")

	def libraries(self):
		return self.filter(type="l")



class PackageRevisionManager(models.Manager):

	def filter_by_slug(self, slug):
		 return self.select_related().filter(package__slug=slug)

