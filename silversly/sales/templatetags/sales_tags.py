from django import template

register = template.Library()

@register.filter(name='sum')
def sum_objects(objects, field):
    try:
        if field:
            return sum(getattr(o, field) for o in objects)
        else:
            return sum(objects)
    except:
        return 0

@register.filter(name='neg')
def negative(object):
    try:
        return -object
    except:
        return 0
