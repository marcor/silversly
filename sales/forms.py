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

class EditVatForm(ModelForm):
    class Meta:
        model = Cart
        fields = ("vat_rate",)

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
        fields = ("year", "number", "date", "payment_method", "costs")
        widgets = {"year": HiddenInput}

    def clean(self):
        cleaned_data = super(InvoiceForm, self).clean()
        date = cleaned_data.get("date")
        number = cleaned_data.get("number")
        if date:
            # default value of invoice.year may not match date.year
            cleaned_data["year"] = date.year - 2000
        if date and number and self.prev_invoice:
            if date.year == self.prev_invoice.date.year and number <= self.prev_invoice.number:
                msg = "Il primo numero disponibile è %d" % (self.prev_invoice.number + 1,)
                self._errors["number"] = self.error_class([msg])
                del cleaned_data["number"]
        return cleaned_data

    def clean_number(self):
        number = self.cleaned_data['number']
        if number < 1:
                raise ValidationError("Dai là, ma che numero è?")
        return number

    def clean_date(self):
        date = self.cleaned_data['date']
        if self.prev_invoice and date < self.prev_invoice.date:
                raise ValidationError("L'ultima fattura è del %s!" % (self.prev_invoice.date.strftime("%d/%m/%Y"),))
        if date.year > datetime.date.today().year:
                raise ValidationError("Ma in che anno siamo!? Devo aver dormito troppo.")
        if getattr(self, "open_ddts", False):
                self.open_ddts = self.open_ddts.exclude(date__gt = date)
                if not self.open_ddts.exists():
                        raise ValidationError("Nessun DDT fino a questa data")
        return date

class PAInvoiceForm(InvoiceForm):
    class Meta(InvoiceForm.Meta):
        model = PAInvoice
        fields = ("year", "number", "date", "refdoc", "refdate", "cig", "payment_method", "costs")
        widgets = {"year": HiddenInput}
