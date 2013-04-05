# -*- coding: utf-8 -*-
from models import *
from django.forms import *

class SellProductForm(ModelForm):
    class Meta:
        model = CartItem
        fields = ("quantity", "discount", "update")

class EditDiscountForm(ModelForm):
    class Meta:
        model = Cart
        fields = ("discount",)

class EditPricelistForm(ModelForm):
    class Meta:
        model = Cart
        fields = ("pricelist",)

class ReceiptForm(ModelForm):
    class Meta:
        model = Scontrino
        fields = ("payed",)

class DdtForm(ModelForm):
    class Meta:
        model = Ddt
        fields = ("number", "shipping_address", "boxes", "appearance")

class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ("number", "date", "payment_method", "costs")
    
    def clean_number(self):
        number = self.cleaned_data['number']
        if self.prev_invoice and number <= self.prev_invoice.number:
                raise ValidationError("Il primo numero disponibile è %d" % (self.prev_invoice.number + 1,))
        return number
    
    def clean_date(self):
        date = self.cleaned_data['date']
        if self.prev_invoice and date < self.prev_invoice.date:
                raise ValidationError("L'ultima fattura è del %s!" % (self.prev_invoice.date.strftime("%d/%m/%Y"),))
        if date.year > datetime.date.today().year:
                raise ValidationError("Ma in che anno siamo!? Devo aver dormito troppo.")
        return date
    
 
