from django import template

register = template.Library()


@register.simple_tag
def getfield(an_object, an_attribute):
    return getattr(an_object, an_attribute)
