from django import template

register = template.Library()

from django.conf import settings

@register.simple_tag()
def silversly_version():
    version = settings.VERSION
    return version