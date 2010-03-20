from django.template import Library

register = Library()

@register.filter
def replace(item, value):
	f, t = value.split(',')
	return item.replace(f,t)
