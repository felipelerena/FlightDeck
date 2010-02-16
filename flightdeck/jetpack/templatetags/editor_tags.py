from django import template
#from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def content_link_id(item):
	return "%s_content" % item.slug


@register.filter
def manifest_link_id(item):
	return "%s_manifest" % item.slug


@register.filter
def dependency_link_id(item):
	return "dependency_%s" % item.slug


@register.filter
def recently_modified_link_id(item):
	return "modified_%s" % item.slug


@register.filter
def render_fullname(item):
	return mark_safe("%s <em>%s</em>" % (item.listname, item.fullname))

