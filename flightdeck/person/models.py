from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	amo_session = models.CharField(max_length=255, blank=True, null=True)
	user = models.ForeignKey(User, unique=True)
