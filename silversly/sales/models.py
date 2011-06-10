# -*- coding: utf-8 -*-
from django.db import models
from inventory.models import Price
from common.models import FixedDecimalField
from decimal import Decimal
import datetime
from django.utils.translation import ugettext_lazy as _
from inventory.models import Pricelist

class CartItem(models.Model):
    cart = models.ForeignKey('Cart')
    product = models.ForeignKey('inventory.Product', verbose_name = _("Prodotto"))
    quantity = models.DecimalField(_(u"Quantità"), max_digits = 7, decimal_places = 2)
    discount = models.PositiveSmallIntegerField(_("Sconto %"), default = 0)
    update = models.BooleanField(_("Scarica dal magazzino"), default = True)

    # these values are written once the transaction is over (cart.current = False)
    # in order to generate correct invoices even after the Product prices have changed.
    final_price = FixedDecimalField(_("Prezzo di vendita al netto di sconti"), max_digits = 7, decimal_places = 2, null=True)
    final_value = FixedDecimalField(_("Valore scontato"), max_digits = 7, decimal_places = 2, null=True)
    final_discount = FixedDecimalField(_("Sconto calcolato"), max_digits = 7, decimal_places = 2, null=True)

    def update_value(self, precision=Decimal(".01")):
        pricelist = self.cart.pricelist
        try:
            price = Price.objects.get(pricelist = pricelist, product = self.product)
        except:
            price = Price(pricelist = pricelist,
                product = self.product,
                method = pricelist.default_method,
                markup = pricelist.default_markup)
        price.update()
        self.final_price = price.gross # * self.quantity
        full_value = (self.final_price * self.quantity).quantize(precision)
        self.final_discount = (full_value * self.discount / 100).quantize(precision)
        self.final_value = full_value - self.final_discount


    def save(self, *args, **kwargs):
        self.update_value()
        super(CartItem, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s%s X %s" % (self.quantity, self.product.unit, self.product)

class Cart(models.Model):
    current = models.BooleanField(default = True)
    customer = models.ForeignKey("people.Customer", verbose_name = _("Cliente"), null = True)
    discount = models.PositiveSmallIntegerField(_("Sconto"), default = 0)
    rounded = models.BooleanField(_("Arrotonda il totale"), default = False)
    pricelist = models.ForeignKey("inventory.Pricelist", default = "Pubblico")

    # same as above, even if this is not really necessary
    final_total = FixedDecimalField(_("Totale"), max_digits = 7, decimal_places = 2, null=True)
    final_discount = FixedDecimalField(_("Sconto calcolato"), max_digits = 7, decimal_places = 2, null=True)

    def discounted_total(self):
        return self.final_total - self.final_discount

    def update_value(self):
        value = Decimal()
        #per_item_discount = Decimal()
        for item in self.cartitem_set.all():
            value += item.final_value
            #per_item_discount += item.final_discount
        self.final_total = value
        self.final_discount = self.final_total * self.discount / 100

    def pricelists(self):
        return Pricelist.objects.all()

class Receipt(models.Model):
    cart = models.OneToOneField(Cart, null=True)

    def child(self):
        try:
            r = self.scontrino
            r.type = "scontrino"
        except:
            try:
                r = self.ddt
                r.type = "ddt"
            except:
                r = self.invoice
                r.type = "invoice"
        return r


def prep(decim):
    return str((decim * 1000).quantize(Decimal("1")))

sep = "\x7f"
def print_article(desc, price, quantity):
    return sep.join(("1", desc[:16], prep(quantity), prep(price), "1", sep, "1", "1")) + sep

def print_discount(discount, markdown):
    return sep.join(("1", "1", "1", sep)) + sep.join((prep(discount), "sconto %d%%" % markdown, "1", sep)) + "-1" + sep

def print_total_discount(discount):
    return sep.join(("1", "1", "1", sep)) + sep.join((prep(discount), "sconto cliente", "1", sep)) + "-1" + sep

class Scontrino(Receipt):
    date = models.DateTimeField(auto_now_add = True, unique = True)
    #cart = models.OneToOneField(Cart)
    due = FixedDecimalField(_(u"Importo da saldare"), max_digits = 7, decimal_places = 2, default = 0)
    payed = FixedDecimalField(_(u"Importo saldato"), max_digits = 7, decimal_places = 2)

    cf = models.CharField(_("Codice fiscale/P.IVA"), max_length=20, blank=True)

    def __unicode__(self):
        return u"Scontrino del %s" % (self.date.strftime("%d/%m (%H:%M)"),)

    def send_to_register(self, close = False):
        filescontrino = open('c:\\scontrini\\scontrino.txt', 'w')
        items = self.cart.cartitem_set.all()
        for item in items:
            filescontrino.write(print_article(item.product.name.encode("iso-8859-1"), item.quantity, item.final_price) + "\n")
            if item.discount:
                filescontrino.write(print_discount(item.final_discount, item.discount) + "\n")
        if self.cart.discount:
            filescontrino.write(print_total_discount(self.cart.final_discount) + "\n")
        filescontrino.close()

    def save(self, *args, **kwargs):
        self.due =  self.cart.discounted_total() - self.payed
        super(Scontrino, self).save(*args, **kwargs)

class Ddt(Receipt):
    year = models.PositiveSmallIntegerField(_("Anno"))
    number = models.PositiveSmallIntegerField(_("Numero"))
    date = models.DateField(auto_now_add = True)
    #cart = models.OneToOneField(Cart)
    main_address = models.TextField(verbose_name = _("Indirizzo"))
    shipping_address = models.TextField(verbose_name = _("Indirizzo di spedizione"), blank=True)
    shipping_date = models.DateTimeField(_("Inizio trasporto"), default = lambda: datetime.datetime.now())

    def __unicode__(self):
        return u"DDT %d/%d del" % (self.year,self.number, self.date)

    class Meta:
        ordering = ['date', 'number']

#class InvoiceItem(models.Model):
#    product = models.ForeignKey('inventory.Product', verbose_name = _("Prodotto"))
#    quantity = models.DecimalField(_(u"Quantità"), max_digits = 7, decimal_places = 2)
#    price = FixedDecimalField(_("Prezzo di vendita"), max_digits = 7, decimal_places = 2)
#    discount = models.PositiveSmallIntegerField(_("Sconto"), default = 0)
#
#    def __unicode__(self):
#        return "%s%s X %s" % (self.quantity, self.product.unit, self.product)

class Invoice(Receipt):
    year = models.PositiveSmallIntegerField(_("Anno"))
    number = models.PositiveSmallIntegerField(_("Numero"))
    date = models.DateField(auto_now_add = True)
    immediate = models.BooleanField(_("Fattura immediata"))
    # used for fatture immediate (cart -> invoice)
    #cart = models.OneToOneField(Cart, null = True)
    # used for fatture differite (cart(s) -> receipt(s) -> invoice)
    receipts = models.ManyToManyField(Receipt, null = True, related_name="proxy_receipt")
    payment_method = models.CharField(_("Metodo di pagamento"), max_length = 50)
    bank = models.OneToOneField('people.Bank', verbose_name=_("Banca d'appoggio"), null=True, blank=True)
    costs = FixedDecimalField(_("Spese bancarie"), max_digits = 7, decimal_places = 2, default = 0)

    def __unicode__(self):
        return u"Fattura %d/%d del %s" % (self.year, self.number, self.date)
