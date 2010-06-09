from django.template import Template, Library, loader, Context, TemplateSyntaxError, Node
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

register = Library()

@register.filter
def version_name(revision, autoescape=None):
	name = "<strong>%s</strong> " % revision.version_name if revision.version_name else ""
	return mark_safe("%srev. %d" % (name, revision.revision_number))
version_name.needs_autoescape = True
