# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import F
from decimal import Decimal
from common.models import FixedDecimalField

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
    
    def clean(self):
        self.name = self.name.strip().lower()

    def breadcrumbs(self):
        anchor = '<a href="%s" title="Mostra i prodotti nella categoria %s">%s</a>' % (self.get_absolute_url(), self.name, self.name)
        if (self.parent is None):
            return anchor
        return "%s > %s" % (self.parent.breadcrumbs(), anchor)
    
    @models.permalink
    def get_absolute_url(self):
        return ('inventory.views.list_by_category', (str(self.id),))

    def total_products(self):
        total = Product.objects.filter(category=self).count()
        for child in Category.objects.filter(parent=self):
            total += child.total_products()
        return total
        
    class Meta:
        ordering = ['name']
        verbose_name = _("Categoria")
        verbose_name_plural = _("Categorie") 

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

    suppliers = models.ManyToManyField('people.Supplier', verbose_name = _("Fornitori"), through = 'Supply', null = True)
    base_price = FixedDecimalField(_("Prezzo base"), max_digits = 8, decimal_places = 2, default = 0)
    prices = models.ManyToManyField(Pricelist, verbose_name = _("Listini"), through = 'Price', null = True)
    
    catalogue = models.BooleanField(verbose_name = _("Includi nel catalogo"), default = False)
        
    def __unicode__(self):
        return self.name

    def add(self, quantity):
        self.quantity += quantity

    def clean(self):
        name = self.name.strip()
        first = name[0]
        if first.isupper():
            self.name = first.lower() + name[1:]
        else:
            self.name = name

    def update_base_price(self):        
        supplies = Supply.objects.filter(product = self)
        if (supplies.count() > 0):
            supplier_prices = [supply.price for supply in supplies]
            self.base_price = (sum(supplier_prices) / len(supplier_prices))
        else:
            self.base_price = 0
        self.save()
        prices = Price.objects.filter(product = self).exclude(method = "==")
        for price in prices:
            price.update()
            price.save()
    
    class Meta:
        verbose_name = _("Articolo")
        verbose_name_plural = _("Articoli")
        ordering = ['name', 'code']

class IncomingProduct(models.Model):
    actual_product = models.ForeignKey('Product', null=True, blank=True)
    batch = models.ForeignKey('BatchLoad')
    
    quantity = models.DecimalField(_(u"Quantità da aggiungere"), max_digits = 8, decimal_places = 3)
    
    new_supplier_code = models.CharField(_("Codice fornitore"), max_length = 20, null = True, blank = True)
    new_supplier_price = FixedDecimalField(_("Prezzo di acquisto"), max_digits = 8, decimal_places = 3)

    base_price = FixedDecimalField(_("Prezzo base"), max_digits = 8, decimal_places = 3, default = 0)
    new_prices = models.ManyToManyField(Pricelist, verbose_name = _("Listini"), through = 'NewPrice', null = True)

    def clean(self):
        supplies = Supply.objects.filter(product = self.actual_product).exclude(supplier = self.batch.supplier)
        self.new_supplier_price = self.new_supplier_price or 0
        if supplies:
            self.base_price = sum([supply.price for supply in supplies], self.new_supplier_price) / (len(supplies) + 1)
        else:
            self.base_price = self.new_supplier_price

    class Meta:
        unique_together = ['batch', 'actual_product']

class AbstractPrice(models.Model):
    method = models.CharField(_("Tipo di prezzo"), max_length = 2, choices = PRICE_MAKING_METHODS)
    gross = FixedDecimalField(_("Prezzo con IVA"), max_digits = 7, decimal_places = 2)
    net = FixedDecimalField(_("Prezzo netto"), max_digits = 7, decimal_places = 2, null = True)     
    markup = models.PositiveSmallIntegerField(_("Percentuale ricarico"), null = True)
    pricelist = models.ForeignKey(Pricelist, verbose_name = _("Listino"))
    
    def __init__(self, *args, **kwargs):
        super(AbstractPrice, self).__init__(*args, **kwargs)
        if self.pk is None:
            self.update()
        
    def __unicode__(self):
        if self.method == '==':
            return unicode(self.gross)
        else:
            return u"+%s%%" % self.markup
    
    def update(self, taxes=20, default_precision=Decimal(".01")):
        if self.method == "%=":
            self.gross = (self.product.base_price * Decimal(str((100 + self.markup) * (100 + taxes))) / 10000)
        elif self.method == "%~":
            estimated_net = self.product.base_price * Decimal(str(100 + self.markup)) / 100
            gross = (estimated_net * Decimal(str(100 + taxes)) / 100)
            if gross <= .25:
                module = Decimal('.01')
            elif gross <= 1:
                module = Decimal('.05')
            elif gross < 10:
                module = Decimal('.2')
            elif gross < 100:
                module = Decimal('.5')
            else:
                module = Decimal('1')
            corrected_price = gross  + module / 2 # this guarantees that the price gets always rounded up
            self.gross = (corrected_price - corrected_price.remainder_near(module))
        
        self.net = (self.gross / 6 * 5)
    
    def save(self, *args, **kwargs):
        self.update()       
        super(AbstractPrice, self).save(*args, **kwargs)            
    
    class Meta:
        abstract = True
        verbose_name = _("Prezzo di vendita")
        verbose_name_plural = _("Prezzi di vendita")
        unique_together = ('pricelist', 'product')
        
class NewPrice(AbstractPrice):
    product = models.ForeignKey(IncomingProduct, verbose_name = _("Prodotto"))
    reset_pricelist_default = models.BooleanField(default = False)
    
    def save(self, *args, **kwargs):
        if self.reset_pricelist_default:
            self.markup = self.pricelist.default_markup
            self.method = self.pricelist.default_method
        super(NewPrice, self).save(*args, **kwargs)   

class Price(AbstractPrice):
    product = models.ForeignKey(Product, verbose_name = _("Prodotto"))

class BatchLoad(models.Model):
    supplier = models.ForeignKey('people.Supplier', verbose_name = _("Fornitore"), related_name="product_batch", null=True)
    document_ref = models.CharField(_(u"Fattura n°"), max_length=5, blank=True) 
    date = models.DateField(auto_now = True)
    loaded = models.BooleanField(default = False)

MOVEMENTS = (
    (u'L', _(u"Carico")),
    (u'U', _(u"Scarico"))
)

class LogEntry(models.Model):
    type = models.CharField(max_length = 1, choices = MOVEMENTS)
    product = models.ForeignKey(Product, verbose_name = _("Prodotto"))
    supplier = models.ForeignKey('people.Supplier', verbose_name = _("Fornitore"), null = True)
    price = FixedDecimalField(_("Prezzo di acquisto"), max_digits = 8, decimal_places = 3, null = True)
    quantity = models.DecimalField(_(u"Quantità acquistata"), max_digits = 8, decimal_places = 3)
    date = models.DateTimeField(auto_now = True)

class Supply(models.Model):
    product = models.ForeignKey(Product, verbose_name = _("Prodotto"))
    supplier = models.ForeignKey('people.Supplier', verbose_name = _("Fornitore"))
    code = models.CharField(_("Codice fornitore"), max_length = 20, null = True, blank = True)
    price = FixedDecimalField(_("Prezzo di acquisto"), max_digits = 8, decimal_places = 3)
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

    def delete(self, *args, **kwargs):
        super(Supply, self).delete(*args, **kwargs)
        # we don't update the quantity, only the price
        self.product.update_base_price()

    class Meta:
        verbose_name = _("Fornitura")
        verbose_name_plural = _("Forniture")
        unique_together = ('product', 'supplier')
