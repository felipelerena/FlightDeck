from django.db.models.manager import Manager

def get_object_or_create(klass, *args, **kwargs):
	if isinstance(klass, Manager):
		manager = klass
		klass = manager.model
	else:
		manager = klass._default_manager
	try:
		return manager.get(*args, **kwargs)
	except klass.DoesNotExist:
		return manager.create(*args, **kwargs)

