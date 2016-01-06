from django import template
from django.template import TemplateSyntaxError, Variable, Node, Variable, Library
from django.conf import settings

import re

register = template.Library()

from django.conf import settings

@register.filter
def split_addr(s):
    m = re.match(getattr(settings, "ADDRESS_FORMAT"), s)
    return {
        'street': m.group(1),
        'pcode': m.group(2),
        'city': m.group(3),
        'prov': m.group(4)
    }

@register.filter
def modulo(num, val):
    return num % val

@register.filter(name='roundup_divide')
def roundup_divide(items, items_per_page):
	try:
		return (items - 1) // items_per_page + 1
	except:
		return (len(items) - 1) // items_per_page + 1

@register.filter
def divide(num, val):
    return num // val

@register.filter(name='times')
def times(number):
    return range(number)

@register.filter(name='linepad')
def linepad(total_lines, available_lines_per_page):
    lines_on_last_page = total_lines % available_lines_per_page
    if  lines_on_last_page == 0:
        return 0
    else:
        return available_lines_per_page - lines_on_last_page

@register.simple_tag()
def silversly_version():
    version = settings.VERSION
    return version

@register.simple_tag()
def debug():
    return settings.DEBUG

# thanks to pklaus:

# I found some tricks in URLNode and url from defaulttags.py:
# https://code.djangoproject.com/browser/django/trunk/django/template/defaulttags.py
@register.tag
def value_from_settings(parser, token):
  bits = token.split_contents()
  if len(bits) < 2:
    raise TemplateSyntaxError("'%s' takes at least one " \
      "argument (settings constant to retrieve)" % bits[0])
  settingsvar = bits[1]
  settingsvar = settingsvar[1:-1] if settingsvar[0] == '"' else settingsvar
  asvar = None
  bits = bits[2:]
  if len(bits) >= 2 and bits[-2] == 'as':
    asvar = bits[-1]
    bits = bits[:-2]
  if len(bits):
    raise TemplateSyntaxError("'value_from_settings' didn't recognise " \
      "the arguments '%s'" % ", ".join(bits))
  return ValueFromSettings(settingsvar, asvar)

class ValueFromSettings(Node):
  def __init__(self, settingsvar, asvar):
    self.arg = Variable(settingsvar)
    self.asvar = asvar
  def render(self, context):
    ret_val = getattr(settings,str(self.arg))
    if self.asvar:
      context[self.asvar] = ret_val
      return ''
    else:
      return ret_val
