# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import F
from decimal import Decimal
import datetime


PRICE_MAKING_METHODS = (
    (u'==', _(u"Fisso")),
    (u'%=', _(u"% ricarico")),
    (u'%~', _(u"% ricarico con arrotond."))
)

VARIABLE_PRICE_MAKING_METHODS = (
    (u'%=', _(u"% ricarico")),
    (u'%~', _(u"% ricarico con arrotondamento"))
)

class Category(models.Model):
    name = models.CharField(_("Nome"), max_length = 60)
    parent = models.ForeignKey('Category', verbose_name = _("Categoria madre"), blank = True, null = True)

    def __unicode__(self):
        if (self.parent is None):
            return self.name
        return "%s > %s" % (self.parent, self.name)

    def breadcrumbs(self):
        anchor = '<a href="%s" title="Mostra i prodotti nella categoria %s">%s</a>' % (self.get_absolute_url(), self.name, self.name)
        if (self.parent is None):
            return anchor
        return "%s > %s" % (self.parent.breadcrumbs(), anchor)

    def get_absolute_url(self):
        return "/categoria/%i/" % self.id

    def total_products(self):
        total = Product.objects.filter(category=self).count()
        for child in Category.objects.filter(parent=self):
            total += child.total_products()
        return total
        
    class Meta:
        ordering = ['name']
        verbose_name = _("Categoria")
        verbose_name_plural = _("Categorie")

class Bank(models.Model):
    name = models.CharField(_("Descrizione"), max_length=50)
    abi = models.CharField(_("ABI"), max_length = 5)
    cab = models.CharField(_("CAB"), max_length = 5)
    
    def __unicode__(self):
        return self.name

class Address(models.Model):
    street = models.CharField(_("Indirizzo"), max_length = 50)
    city = models.CharField(_("Città"), max_length=30)
    province = models.CharField(_("Provincia"), max_length=2)
    postcode = models.CharField(_("CAP"), max_length=5)    

class Supplier(models.Model):
    name = models.CharField(_("Nome"), max_length = 50, unique=True)
    phone = models.CharField(_("Telefono"), max_length=15, default=None, blank=True)
    fax = models.CharField(_("Fax"), max_length=15, default=None, blank=True)
    email = models.CharField(_("E-mail"), max_length=30, default=None, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
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

class Pricelist(models.Model):
    name = models.CharField(_("Nome"), max_length = 25, primary_key = True)
    default_method = models.CharField(_("Tipo di prezzo"), max_length = 2, choices = VARIABLE_PRICE_MAKING_METHODS)
    default_markup = models.PositiveSmallIntegerField(_("Percentuale ricarico di default"))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Listino")
        verbose_name_plural = _("Listini")

class Product(models.Model):
    code = models.CharField(_("Codice"), max_length = 13)
    name = models.CharField(_("Nome"), max_length = 60, unique = True)

    quantity = models.DecimalField(_(u"Quantità"), max_digits = 8, decimal_places = 3, default = 0)
    min_quantity = models.DecimalField(_(u"Scorta minima"), max_digits = 8, decimal_places = 3, default = 0)
    unit = models.CharField(_(u"Unità di misura"), max_length = 15)

    category = models.ForeignKey(Category, verbose_name = _("Categoria"))

    suppliers = models.ManyToManyField(Supplier, verbose_name = _("Fornitori"), through = 'Supply', null = True)
    base_price = models.DecimalField(_("Prezzo base"), max_digits = 8, decimal_places = 3, default = 0)
    prices = models.ManyToManyField(Pricelist, verbose_name = _("Listini"), through = 'Price', null = True)

    def __unicode__(self):
        return self.name

    def add(self, quantity):
        self.quantity += quantity

    def update_base_price(self):        
        supplies = Supply.objects.filter(product = self)
        if (supplies.count() > 0):
            supplier_prices = [supply.price for supply in supplies]
            self.base_price = (sum(supplier_prices) / len(supplier_prices)).quantize(Decimal('.001'))
        else:
            self.base_price = 0
        print "base price: " + str(self.base_price)
        self.save()
    
    class Meta:
        verbose_name = _("Articolo")
        verbose_name_plural = _("Articoli")
        ordering = ['name', 'code']

class CartItem(models.Model):
    cart = models.ForeignKey('Cart')
    product = models.ForeignKey(Product, verbose_name = _("Prodotto"))
    quantity = models.DecimalField(_(u"Quantità"), max_digits = 7, decimal_places = 2)
    discount = models.PositiveSmallIntegerField(_("Sconto"), default = 0)
    update = models.BooleanField(_("Scarica dal magazzino"), default = True)
    
    def __unicode__(self):
        return "%s%s X %s" % (self.quantity, self.product.unit, self.product)

class Cart(models.Model):
    current = models.BooleanField(default = True)
    date = models.DateTimeField(auto_now_add = True)
    
    #def __unicode__(self):
    #    return "%d prodotti, %s" % (self.products.count(), self.current and "aperto" or "chiuso")
        
    class Meta:
        ordering = ['date']
        
class Receipt(models.Model):
    number = models.PositiveIntegerField(_("Numero")) 
    date = models.DateTimeField(auto_now = True)
    cart = models.ForeignKey(Cart)
    customer = models.ForeignKey(RetailCustomer, null=True, blank=True)
    
    def __unicode__(self):
        return "Scontrino %d del %s" % (self.number, self.date)
        
class Ddt(models.Model):
    number = models.PositiveSmallIntegerField(_("Numero"), unique = True) 
    date = models.DateField(auto_now_add = True)
    cart = models.ForeignKey(Cart)
    customer = models.ForeignKey(RetailCustomer, null=True, blank=True)
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
    bank = models.OneToOneField('Bank', verbose_name=_("Banca d'appoggio"), null=True, blank=True)
    costs = models.DecimalField(_("Spese bancarie"), max_digits = 7, decimal_places = 2, default = 0) 
        
class Price(models.Model):
    method = models.CharField(_("Tipo di prezzo"), max_length = 2, choices = PRICE_MAKING_METHODS)
    value = models.DecimalField(_("Prezzo con IVA"), max_digits = 7, decimal_places = 2, null = True) 
    markup = models.PositiveSmallIntegerField(_("Percentuale ricarico"), null = True)
    pricelist = models.ForeignKey(Pricelist, verbose_name = _("Listino"))
    product = models.ForeignKey(Product, verbose_name = _("Prodotto"))

    def __unicode__(self):
        if self.method == '==':
            return unicode(self.value)
        else:
            return "+%s%%" % self.markup
    
    def calculate_price(self, taxes=20, default_precision=Decimal(".01")):
        if self.method == "==":
            full_price = self.value.quantize(default_precision)
        elif self.method == "%=":
            full_price = (self.product.base_price * Decimal(str((100 + self.markup) * (100 + taxes))) / 10000).quantize(default_precision)
        else:
            estimated_net_price = self.product.base_price * Decimal(str(100 + self.markup)) / 100
            full_price = (estimated_net_price * Decimal(str(100 + taxes)) / 100)
            if full_price <= .25:
                module = Decimal('.01')
            elif full_price <= 1:
                module = Decimal('.05')
            elif full_price < 10:
                module = Decimal('.2')
            elif full_price < 100:
                module = Decimal('.5')
            else:
                module = Decimal('1')
            corrected_price = full_price  + module / 2 # this guarantees that the price gets always rounded up
            full_price = (corrected_price - corrected_price.remainder_near(module)).quantize(default_precision)
        
        taxes = (full_price /  6).quantize(default_precision)
        net_price = full_price - taxes
        return {'net': net_price, 'full': full_price, 'tax': taxes}
        
    class Meta:
        verbose_name = _("Prezzo di vendita")
        verbose_name_plural = _("Prezzi di vendita")
        unique_together = ('pricelist', 'product')

MOVEMENTS = (
    (u'L', _(u"Carico")),
    (u'U', _(u"Scarico"))
)

class LogEntry(models.Model):
    type = models.CharField(max_length = 1, choices = MOVEMENTS)
    product = models.ForeignKey(Product, verbose_name = _("Prodotto"))
    supplier = models.ForeignKey(Supplier, verbose_name = _("Fornitore"), null = True)
    price = models.DecimalField(_("Prezzo di acquisto"), max_digits = 8, decimal_places = 3, null = True)
    quantity = models.DecimalField(_(u"Quantità acquistata"), max_digits = 8, decimal_places = 3)
    date = models.DateTimeField(auto_now = True)

class Supply(models.Model):
    product = models.ForeignKey(Product, verbose_name = _("Prodotto"))
    supplier = models.ForeignKey(Supplier, verbose_name = _("Fornitore"))
    code = models.CharField(_("Codice fornitore"), max_length = 20, null = True, blank = True)
    price = models.DecimalField(_("Prezzo di acquisto"), max_digits = 8, decimal_places = 3)
    updated = models.DateField(_("Ultimo acquisto"), auto_now = True)

    def __unicode__(self):
        return u"%s (fornito da %s a %s€)" % (self.product, self.supplier, self.price)
        
    def save(self, *args, **kwargs):
        super(Supply, self).save(*args, **kwargs)

        #if (log):
        #    log_entry = LogEntry(
        #        type = 'L',
        #        product = self.product, 
        #        supplier = self.supplier,
        #        price = self.last_price,
        #        quantity = self.last_quantity)
        #    log_entry.save()
        #    self.product.add(self.last_quantity)

        self.product.update_base_price()
        self.product.save()

    def delete(self, *args, **kwargs):
        super(Supply, self).delete(*args, **kwargs)
        # we don't update the quantity, only the price
        self.product.update_base_price()
        self.product.save()

    class Meta:
        verbose_name = _("Fornitura")
        verbose_name_plural = _("Forniture")
        unique_together = ('product', 'supplier')
