from django import template

register = template.Library()


@register.filter
def split_with(a_string, a_separator):
    return a_string.split(a_separator)
