from django import template

register = template.Library()

@register.filter(name='custom_range')
def custom_range(value):
    return range(value)
