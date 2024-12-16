from django import template

register = template.Library()


@register.filter(name='format_duration')
def format_duration(value):
    if isinstance(value, str):
        return value.split('.')[0]
    return str(value).split('.')[0]
