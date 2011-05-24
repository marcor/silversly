# -*- coding: utf-8 -*-
from django.db import models
from common.models import FixedDecimalField
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

class Bank(models.Model):
    name = models.CharField(_("Descrizione"), max_length=50)
    abi = models.CharField(_("ABI"), max_length = 5)
    cab = models.CharField(_("CAB"), max_length = 5)

    def __unicode__(self):
        return self.name

#class Address(models.Model):
#    street = models.CharField(_("Indirizzo"), max_length = 50)
#    city = models.CharField(_(u"Città"), max_length=30)
#    province = models.CharField(_("Provincia"), max_length=2)
#    postcode = models.CharField(_("CAP"), max_length=5)

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

    def to_dict(self):
        data = {'id': self.id,
            'name': self.name,
            'cf': self.cf or False,
            'due': self.due,
            'url': self.get_absolute_url()}
        try:
            company = self.companycustomer
            data.update(is_company = True,
                piva = company.piva)
        except:
            pass
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

    payment_method = models.CharField(_("Metodo di pagamento"), max_length = 50, default="")
    bank = models.OneToOneField('Bank', verbose_name=_("Banca d'appoggio"), null=True, blank=True)
    costs = FixedDecimalField(_("Spese bancarie"), max_digits = 7, decimal_places = 2, default = 0)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Cliente con P.IVA")
        verbose_name_plural = _("Clienti con P.IVA")
