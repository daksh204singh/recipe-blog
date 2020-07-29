from django import template

register = template.Library()
@register.filter(name='subtract')
def subtract(value1, value2):
    return value1 - value2
