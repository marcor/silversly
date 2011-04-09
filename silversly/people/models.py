# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Bank(models.Model):
    name = models.CharField(_("Descrizione"), max_length=50)
    abi = models.CharField(_("ABI"), max_length = 5)
    cab = models.CharField(_("CAB"), max_length = 5)
    
    def __unicode__(self):
        return self.name

class Address(models.Model):
    street = models.CharField(_("Indirizzo"), max_length = 50)
    city = models.CharField(_(u"Città"), max_length=30)
    province = models.CharField(_("Provincia"), max_length=2)
    postcode = models.CharField(_("CAP"), max_length=5)   
    
class Supplier(models.Model):
    name = models.CharField(_("Nome"), max_length = 50, unique=True)
    phone = models.CharField(_("Telefono"), max_length=15, default=None, blank=True)
    fax = models.CharField(_("Fax"), max_length=15, default=None, blank=True)
    email = models.CharField(_("E-mail"), max_length=30, default=None, blank=True)
    
    def clean(self):
        self.name = self.name.strip().capitalize()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("Fornitore")
        verbose_name_plural = _("Fornitori")

class RetailCustomer(models.Model):
    name = models.CharField(_("Nome"), max_length = 50, unique=True)
    due = models.DecimalField(_(u"Debito"), max_digits = 8, decimal_places = 3, default = 0)
    phone = models.CharField(_("Telefono"), max_length=15, default=None, blank=True)
    email = models.CharField(_("E-mail"), max_length=30, default=None, blank=True)
    
    def __unicode__(self):
        return self.name
        
class Customer(models.Model):
    name = models.CharField(_("Nome"), max_length = 50, unique=True)
    code = models.CharField(_("P. IVA / C. Fiscale"), max_length=20, unique=True)
    
    phone = models.CharField(_("Telefono"), max_length=15, default=None, blank=True)
    email = models.CharField(_("E-mail"), max_length=30, default=None, blank=True)
    
    main_address = models.TextField(verbose_name = _("Indirizzo"))
    shipping_address = models.TextField(verbose_name = _("Indirizzo di spedizione"), null=True, blank=True)
    
    payment_method = models.CharField(_("Metodo di pagamento"), max_length = 50)
    bank = models.OneToOneField('Bank', verbose_name=_("Banca d'appoggio"), null=True, blank=True)
    costs = models.DecimalField(_("Spese bancarie"), max_digits = 7, decimal_places = 2, default = 0) 
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Cliente")
        verbose_name_plural = _("Clienti")
