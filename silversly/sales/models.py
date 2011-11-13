# -*- coding: utf-8 -*-
from django.db import models
from inventory.models import Price
from common.models import *
from decimal import Decimal
import datetime, os
from django.utils.translation import ugettext_lazy as _
from inventory.models import Pricelist
from django.conf import settings
from django.contrib.sites.models import Site

PAYMENT_CHOICES = getattr(settings, 'PAYMENT_CHOICES')
precision = Decimal(".01")

class CartItem(models.Model):
    cart = models.ForeignKey('Cart')
    product = models.ForeignKey('inventory.Product', verbose_name = _("Prodotto"))
    quantity = models.DecimalField(_(u"Quantità"), max_digits = 7, decimal_places = 2)
    discount = models.PositiveSmallIntegerField(_("Sconto %"), default = 0)
    update = models.BooleanField(_("Scarica dal magazzino"), default = True)

    # these values are written once the transaction is over (cart.current = False)
    # in order to generate correct invoices even after the Product prices have changed.
    final_net_price = FixedDecimalField(_("Prezzo di vendita al netto di sconti e IVA"), max_digits = 7, decimal_places = 2, null=True)
    final_price = FixedDecimalField(_("Prezzo di vendita al netto di sconti"), max_digits = 7, decimal_places = 2, null=True)

    def update_value(self, precision=Decimal(".01")):
        pricelist = self.cart.pricelist
        try:
            price = Price.objects.get(pricelist = pricelist, product = self.product)
        except:
            price = Price(pricelist = pricelist,
                product = self.product,
                method = pricelist.default_method,
                markup = pricelist.default_markup)
            # is this ok?
            price.update()

        self.final_net_price = price.net
        self.final_price = price.gross

    def net_total(self):
        return self.total(net = True)

    def gross_total(self):
        return self.total(net = False)

    def total(self, net=False):
        if net:
            price = self.final_net_price
        else:
            price = self.final_price
        total = price * self.quantity
        discount = (total * self.discount / 100).quantize(precision)
        value = (total - discount).quantize(precision)
        return (value, discount)

    def save(self, *args, **kwargs):
        self.update_value()
        super(CartItem, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s%s X %s" % (self.quantity, self.product.unit, self.product)

    class Meta:
        ordering = ["-id"]

def rounded(value):
    if value < 10:
        remainder = value.remainder_near(Decimal(".1"))
    else:
        remainder = value.remainder_near(Decimal(".5"))
    return remainder

def apply_vat(value):
    total = (value * Decimal(str(100 + settings.TAX)) / 100).quantize(precision)
    # valore ivato e iva
    return (total, total - value)

class Cart(models.Model):
    current = models.BooleanField(default = True)
    customer = models.ForeignKey("people.Customer", verbose_name = _("Cliente"), null = True)
    discount = models.PositiveSmallIntegerField(_("Sconto"), default = 0)
    rounded = models.BooleanField(_("Arrotonda il totale"), default = True)
    pricelist = models.ForeignKey("inventory.Pricelist", default = "Pubblico")

    # same as above, even if this is not really necessary

    final_net_total = FixedDecimalField(_("Totale netto"), max_digits = 7, decimal_places = 2, null=True)
    final_net_discount = FixedDecimalField(_("Sconto netto calcolato"), max_digits = 7, decimal_places = 2, null=True)

    final_total = FixedDecimalField(_("Totale"), max_digits = 7, decimal_places = 2, null=True)
    final_discount = FixedDecimalField(_("Sconto calcolato"), max_digits = 7, decimal_places = 2, null=True)

    def discounted_total(self):
        return self.final_total - self.final_discount

    def discounted_net_total(self):
        return self.final_net_total - self.final_net_discount

    def apply_vat(self):
        return apply_vat(self.discounted_net_total())

    def apply_rounding(self):
            # works only to scontrini for the time being
            round_value = rounded(self.discounted_total())
            self.final_discount += round_value

    def update_value(self, deep = False):
        items = self.cartitem_set.all()
        if deep:
            for item in items:
                item.update_value()
                item.save()

        gross_value = Decimal()
        net_value = Decimal()

        for item in items:
            net_value += item.total(net = True)[0]
            gross_value += item.total(net = False)[0]

        self.final_total = gross_value
        self.final_discount = self.final_total * self.discount / 100

        if self.rounded:
            self.apply_rounding()

        self.final_net_total = net_value
        self.final_net_discount = self.final_net_total * self.discount / 100

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

    class Meta:
        ordering = ["-id"]


def prep(decim):
    return str((decim * 1000).quantize(Decimal("1")))

sep = settings.RECEIPT_SEPARATOR
def print_article(desc, price, quantity):
    return sep.join(("1", desc[:16], prep(quantity), prep(price), "1", sep, "1", "1")) + sep

def print_discount(discount, markdown):
    return sep.join(("1", "1", "1", sep)) + sep.join((prep(discount), "sconto %d%%" % markdown, "1", sep)) + "-1" + sep

def print_total_discount(discount, desc="sconto cliente"):
    return sep.join(("1", "1", "1", sep)) + sep.join((prep(discount), "sconto cliente", "1", sep)) + "-1" + sep

def print_rounding(tot):
    if tot > 0:
        return print_total_discount(tot, "arrotondamento")
    else:
        return print_article("arrotondamento", -tot, Decimal(1))

def close_receipt():
    return sep.join(("0","1")) + (sep * 8)

class Scontrino(Receipt):
    date = models.DateTimeField(auto_now_add = True, unique = True)
    #cart = models.OneToOneField(Cart)
    due = FixedDecimalField(_(u"Importo da saldare"), max_digits = 7, decimal_places = 2, default = 0)
    payed = FixedDecimalField(_(u"Importo saldato"), max_digits = 7, decimal_places = 2)

    cf = models.CharField(_("Codice fiscale/P.IVA"), max_length=20, blank=True)

    def __unicode__(self):
        return u"Scontrino del %s" % (self.date.strftime("%d/%m (%H:%M)"),)

    def send_to_register(self, close = None):
        options = Settings.objects.get(site = Site.objects.get_current())
        if close is None:
            close = options.close_receipts
        filescontrino = open(os.path.join(options.receipt_folder, 'scontrino.txt'), 'w')
        items = self.cart.cartitem_set.all()
        for item in items:
            total, discount = item.total(net=False)
            filescontrino.write(print_article(item.product.name.encode("iso-8859-1"), item.quantity, item.final_price) + "\n")
            if item.discount:
                filescontrino.write(print_discount(discount, item.discount) + "\n")
        if self.cart.discount:
            filescontrino.write(print_total_discount(self.cart.final_discount) + "\n")
        elif self.cart.rounded and self.cart.final_discount:
            filescontrino.write(print_rounding(self.cart.final_discount) + "\n")
        if close:
            filescontrino.write(close_receipt() + "\n")
        filescontrino.close()

    def finally_paid(self):
        if self.cart.customer:
            self.cart.customer.due -= self.due
            self.cart.customer.save()
        self.payed += self.due
        self.save()

    def save(self, *args, **kwargs):
        # we assume that save is called at most twice:
        # the second time around by finally_paid()
        self.due = self.cart.discounted_total() - self.payed
        if self.due and self.cart.customer:
            self.cart.customer.due += self.due
            self.cart.customer.save()
        super(Scontrino, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return('sales.views.show_receipt', [str(self.id)])



class Ddt(Receipt):
    year = models.PositiveSmallIntegerField(_("Anno"), default = lambda: datetime.date.today().year - 2000)
    number = models.PositiveSmallIntegerField(_("Numero"))
    date = models.DateField(auto_now_add = True)

    main_address = models.TextField(verbose_name = _("Indirizzo"))
    shipping_address = models.TextField(verbose_name = _("Indirizzo di spedizione"), blank=True)
    shipping_date = models.DateTimeField(_("Inizio trasporto"), default = lambda: datetime.datetime.now())

    boxes = models.PositiveSmallIntegerField(_(u"N° colli"), null = True, blank = True)
    appearance = models.CharField(_(u"Aspetto"), max_length = 20, null = True, blank = True)

    # used for fatture differite (cart(s) -> receipt(s) -> invoice)
    invoice = models.ForeignKey('Invoice', verbose_name = _("Fattura"), null = True)

    def __unicode__(self):
        return u"DDT %d/%d del %s" % (self.year,self.number, self.date.strftime("%d/%m"))

    @models.permalink
    def get_absolute_url(self):
        return('sales.views.show_ddt', [str(self.id)])

    def date_short(self):
        return self.date.strftime("%d/%m/%y")

    def shipping_date_short(self):
        return self.shipping_date.strftime("%H:%M %d/%m/%y")

    class Meta:
        ordering = ['-year', '-date', '-number']

class Invoice(Receipt):
    year = models.PositiveSmallIntegerField(_("Anno"), default = lambda: datetime.date.today().year - 2000)
    number = models.PositiveSmallIntegerField(_("Numero"))
    date = models.DateField(_("Data fattura"), default = lambda: datetime.datetime.now())
    immediate = models.BooleanField(_("Fattura immediata"))
    # used for fatture immediate (cart -> invoice)
    # cart = models.OneToOneField(Cart, null = True)

    payment_method = models.CharField(_("Metodo di pagamento"), max_length = 4, choices = PAYMENT_CHOICES)
    costs = FixedDecimalField(_("Spese incasso"), max_digits = 7, decimal_places = 2, default = Decimal(settings.BANK_COST))

    total_net = FixedDecimalField(_("Imponibile"), max_digits = 8, decimal_places = 2, null = True)
    payed = models.BooleanField(_("Pagata"), default = False)

    def __unicode__(self):
        return u"Fattura %d/%d del %s" % (self.year, self.number, self.date.strftime("%d/%m"))

    def finally_paid(self):
        due = self.apply_vat()[0]
        if self.immediate:
            customer = self.cart.customer
        else:
            customer = self.ddt_set.all()[0].cart.customer
        customer.due -= due
        customer.save()
        self.payed = True
        self.save()

    @models.permalink
    def get_absolute_url(self):
        return('sales.views.show_invoice', [str(self.id)])

    def apply_vat(self):
        return apply_vat(self.total_net)

    class Meta:
        ordering = ['-year', '-date', '-number']
