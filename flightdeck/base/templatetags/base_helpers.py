from django.template import Template, Library, loader, Context, TemplateSyntaxError, Node
from django.template.defaultfilters import escapejs

register = Library()

@register.filter
def replace(item, value):
	f, t = value.split(',')
	return item.replace(f,t)


@register.tag
def escape_template(parser, token):
    try:
        tag_name, template_name = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError, \
				"%r tag requires exactly one argument" % token.contents.split()[0]
    if not (template_name[0] == template_name[-1] and template_name[0] in ('"', "'")):
        raise TemplateSyntaxError, \
				"%r tag's argument should be in quotes" % tag_name
    return EscapeTemplate(template_name[1:-1])

class EscapeTemplate(Node):
    def __init__(self, template_name):
		self.t = loader.get_template(template_name)

    def render(self, context):
		return escapejs(self.t.render(context))

