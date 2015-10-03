from django.db import models
from decimal import Decimal, InvalidOperation
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

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
        except TypeError: 
            # Decimal(value) doesn't work when value is a Decimal object after 
            # the decimal module has been reloaded. 
            if hasattr(value, 'as_tuple'): 
                return Decimal(value.as_tuple()) 
            raise 
            

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^common\.models\.FixedDecimalField"])

class Shop(models.Model):
    site = models.OneToOneField(Site, default = lambda: Site.objects.get_current())

    name = models.CharField(u"Ragione sociale", max_length = 60)
    piva = models.CharField(_("P. IVA"), max_length=20)
    cf = models.CharField(_("Codice Fiscale"), max_length=16)
    main_address = models.TextField(verbose_name = _("Indirizzo"))

    phone = models.CharField(_("Telefono"), max_length=20)
    email = models.CharField(_("E-mail"), max_length=30)

    bank = models.CharField(_("Banca d'appoggio"), max_length=60)
    iban = models.CharField(_("IBAN"), max_length=30)


class Settings(models.Model):
    site = models.OneToOneField(Site, default = lambda: Site.objects.get_current())

    # cash register stuff
    close_receipts = models.BooleanField(u"Chiudi scontrini", default = True)
    receipt_folder = models.CharField(u"Cartella scontrini", max_length = 60, default="c:\\Scontrini")

