from django.db import models
from decimal import Decimal, InvalidOperation

class FixedDecimalField(models.DecimalField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.unit = Decimal("." + "1" * kwargs["decimal_places"])
        super(FixedDecimalField, self).__init__(*args, **kwargs)
        
    def to_python(self, value):
        if value is None:
            return value
        try:
            return Decimal(value).quantize(self.unit)
        except InvalidOperation:
            raise exceptions.ValidationError(self.error_messages['invalid'])

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^common\.models\.FixedDecimalField"])