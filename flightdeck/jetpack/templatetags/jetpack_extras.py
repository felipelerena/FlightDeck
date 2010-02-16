from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def tab_link_id(item, value):
	return "%s_%s" % (item.slug, value)

@register.filter
def dependency_link_id(item):
	return "dependency_%s" % item.slug


@register.filter
def recently_modified_link_id(item):
	return "modified_%s" % item.slug


@register.filter
def render_fullname(item):
	return mark_safe("%s <em>%s</em>" % (item.listname, item.fullname))

