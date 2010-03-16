from django.db import models
from django.contrib.auth.models import User


class Limit(models.Model):
	email = models.CharField(max_length=255)


class Profile(models.Model):
	user = models.ForeignKey(User, unique=True)
	nickname = models.CharField(max_length=255, blank=True, null=True)
	location = models.CharField(max_length=255, blank=True, null=True)
	occupation = models.CharField(max_length=255, blank=True, null=True)
	homepage = models.CharField(max_length=255, blank=True, null=True)
	photo = models.CharField(max_length=255, blank=True, null=True)

	def get_name(self):
		if not (self.user.first_name or self.user.last_name or self.nickname):
			return self.user.username
		return self.get_fullname()


	def get_fullname(self):
		name = self.user.first_name if self.user.first_name else None
		if self.user.last_name:
			name = '%s %s' % (name, self.user.last_name) if name else self.user.last_name
		if not name and self.nickname:
			return self.nickname
		return name

		
	def __unicode__(self):
		return self.get_name()
