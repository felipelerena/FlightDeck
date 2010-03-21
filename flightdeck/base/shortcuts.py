from random import choice

from django.db.models.manager import Manager
from django.shortcuts import _get_queryset
from django.http import Http404

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


def get_object_with_related_or_404(klass, *args, **kwargs):
    """
    Uses get() to return an object, or raises a Http404 exception if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), an MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass).select_related()
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise Http404('No %s matches the given query.' % queryset.model._meta.object_name)

def get_random_string(number=10, prefix=''):
	allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
	if prefix:
		prefix = '%s-' % prefix
	return '%s%s' % (prefix, ''.join([choice(allowed_chars) for i in range(number)]))
	
