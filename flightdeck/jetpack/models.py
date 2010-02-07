from django.db import models
from django.contrib.auth.models import User


class Jetpack(models.Model):
	PERMISSIONS_CHOICEiS = (
		(0, 'denied'),
		(1, 'view'),
		(2, 'edit'),
	)

	name = models.CharField(max_length=255)
	decription = models.TextField(blank=True, null=True)
	author = models.ForeignKey(User, related_name="authored_jetpacks")
	managers = models.ManyToManyField(User, related_name="managed_jetpacks")
	developers = models.ManyToManyField(User, related_name="developed_jetpacks")
	public_permission = models.IntegerField(choices=PERMISSIONS_CHOICEiS)
	group_permission  = models.IntegerField(choices=PERMISSIONS_CHOICEiS)



STATUS_CHOICES = (
	('a', 'alpha'),
	('b', 'beta'),
	('p', 'production')
)

class Version(models.Model):
	jetpack = models.ForeignKey(Jetpack, related_name="versions")
	name = models.CharField(max_length=255)
	decription = models.TextField(blank=True, null=True)
	code = models.TextField(blank=True, null=True)
	status = models.CharField(max_length=1, choices=STATUS_CHOICES) 
	published = models.BooleanField(default=False, blank=True)


