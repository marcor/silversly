from django import template

register = template.Library()

@register.filter(name='sum')
def sum_objects(objects, field=None):
    try:
        if field:
            attr = getattr(objects[0], field)
            print attr
            if callable(attr):
                return sum(getattr(o, field)() for o in objects)
            else:
                return sum(getattr(o, field) for o in objects)
        else:
            return sum(objects)
    except:
        return 0

@register.filter(name='exactAdd')
def exact_add(object, arg):
    try:
        return object + arg
    except:
        return 0

@register.filter(name='exactSub')
def exact_sub(object, arg):
    try:
        return object - arg
    except:
        return 0

@register.filter(name='neg')
def negative(object):
    try:
        return -object
    except:
        return 0
