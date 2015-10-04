# -*- coding: utf-8 -*-
from django.db import models
from common.models import FixedDecimalField
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings

import simplejson

PAYMENT_CHOICES = getattr(settings, 'PAYMENT_CHOICES')

class Bank(models.Model):
    name = models.CharField(_("Descrizione"), max_length=50)
    abi = models.CharField(_("ABI"), max_length = 5)
    cab = models.CharField(_("CAB"), max_length = 5)

    def __unicode__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(_("Nome"), max_length = 50, unique=True)
    phone = models.CharField(_("Telefono"), max_length=15, default=None, blank=True)
    fax = models.CharField(_("Fax"), max_length=15, default=None, blank=True)
    email = models.CharField(_("E-mail"), max_length=30, default=None, blank=True)

    def clean(self):
        self.name = self.name.strip().capitalize()

    def __unicode__(self):
        return self.name

    def to_dict(self):
        data = {'id': self.id,
            'name': self.name,
            'url': self.get_absolute_url()}
        return data

    def get_absolute_url(self):
        return reverse("show_supplier", args=(self.id,))

    class Meta:
        ordering = ["name"]
        verbose_name = _("Fornitore")
        verbose_name_plural = _("Fornitori")

class Customer(models.Model):
    name = models.CharField(_("Nome"), max_length = 50, unique=True)
    cf = models.CharField(_("Codice fiscale"), max_length=20, blank=True)
    phone = models.CharField(_("Telefono"), max_length=15, blank=True)
    email = models.EmailField(_("E-mail"), max_length=30, blank=True)

    pricelist = models.ForeignKey("inventory.Pricelist", verbose_name = _("Listino associato"), default="Pubblico")
    discount = models.PositiveSmallIntegerField(_("Sconto cliente"), default = 0)
    due = FixedDecimalField(_(u"In debito di €"), max_digits = 8, decimal_places = 2, default = 0)

    def __unicode__(self):
        return self.name

    def child(self):
        try:
            r = self.companycustomer
            try:
                r = r.pacustomer
            except PACustomer.DoesNotExist:
                pass
        except CompanyCustomer.DoesNotExist:
            r = self
        return r
        
    def typename(self):
        return self.__class__.__name__
        
    def is_retail(self):
        return self.__class__ == Customer

    def json(self):
        from common.views import DecimalEncoder

        return simplejson.dumps(self.to_dict(), cls=DecimalEncoder)

    def to_dict(self):
        try:
            data = {'id': self.id,
                'name': self.name,
                'cf': self.cf or False,
                'due': self.due,
                'url': self.get_absolute_url(),
                'is_company': not self.is_retail()
            }
            if not self.is_retail:
                data.update(piva = self.piva)
        except:
            data = self.child().to_dict()
        return data

    def get_absolute_url(self):
        return reverse("show_customer", args=(self.id,))

    class Meta:
        verbose_name = _("Cliente privato")
        verbose_name_plural = _("Clienti privati")


class CompanyCustomer(Customer):
    piva = models.CharField(_("P. IVA"), max_length=20, unique=True)

    main_address = models.TextField(verbose_name = _("Indirizzo"))
    shipping_address = models.TextField(verbose_name = _("Indirizzo di spedizione"), blank=True)

    payment_method = models.CharField(_("Metodo di pagamento"), max_length = 4, choices = PAYMENT_CHOICES, default="30fm")
    bank = models.OneToOneField('Bank', verbose_name=_("Banca d'appoggio"), null=True, blank=True)
    costs = FixedDecimalField(_("Spese bancarie"), max_digits = 7, decimal_places = 2, default = 0)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Cliente con P.IVA")
        verbose_name_plural = _("Clienti con P.IVA")

class PACustomer(CompanyCustomer):
    cu = models.CharField(_("Codice Univoco"), max_length=6, unique=True)
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Ente pubblico")
        verbose_name_plural = _("Enti pubblici")

