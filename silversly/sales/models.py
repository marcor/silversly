# -*- coding: utf-8 -*-
from django.db import models
from common.models import FixedDecimalField
import datetime
from django.utils.translation import ugettext_lazy as _

class CartItem(models.Model):
    cart = models.ForeignKey('Cart')
    product = models.ForeignKey('inventory.Product', verbose_name = _("Prodotto"))
    quantity = models.DecimalField(_(u"Quantità"), max_digits = 7, decimal_places = 2)
    discount = models.PositiveSmallIntegerField(_("Sconto"), default = 0)
    update = models.BooleanField(_("Scarica dal magazzino"), default = True)
    
    def __unicode__(self):
        return "%s%s X %s" % (self.quantity, self.product.unit, self.product)

class Cart(models.Model):
    current = models.BooleanField(default = True)
        
class Receipt(models.Model):
    year = models.PositiveSmallIntegerField(_("Anno"))
    number = models.PositiveIntegerField(_("Numero")) 
    date = models.DateTimeField(auto_now = True)
    cart = models.OneToOneField(Cart)
    customer = models.ForeignKey('people.RetailCustomer', null=True, blank=True)
    
    def __unicode__(self):
        return "Scontrino %d del %s" % (self.number, self.date)
        
    class Meta:
        unique_together = ('year', 'number')
        
class Ddt(models.Model):
    number = models.PositiveSmallIntegerField(_("Numero"), unique = True) 
    date = models.DateField(auto_now_add = True)
    cart = models.ForeignKey(Cart)
    customer = models.ForeignKey('people.RetailCustomer', null=True, blank=True)
    main_address = models.TextField(verbose_name = _("Indirizzo"))
    shipping_address = models.TextField(verbose_name = _("Indirizzo di spedizione"), null=True, blank=True)
    shipping_date = models.DateTimeField(_("Inizio trasporto"), default = lambda: datetime.datetime.now())
    
    def __unicode__(self):
        return "DDT n° %d del %s" % (self.number, self.date)
        
    class Meta:
        ordering = ['date', 'number']
        
class Invoice(models.Model):
    number = models.PositiveSmallIntegerField(_("Numero"), unique = True) 
    ddts = models.ManyToManyField(Ddt)
    payment_method = models.CharField(_("Metodo di pagamento"), max_length = 50)
    bank = models.OneToOneField('people.Bank', verbose_name=_("Banca d'appoggio"), null=True, blank=True)
    costs = FixedDecimalField(_("Spese bancarie"), max_digits = 7, decimal_places = 2, default = 0) 
