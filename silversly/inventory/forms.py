# -*- coding: utf-8 -*-
from django.forms import ModelForm, Form, BooleanField, ChoiceField, RadioSelect, HiddenInput
from decimal import Decimal
from models import *

class QuantityForm(ModelForm):

    # if we are dealing with fractioned products enforce integral quantities
    def check_integral_quantity(product, fieldnames):
        if product.factor:
            for field in fieldnames:
                quantity = self.cleaned_data.get(field)
                if quantity and quantity.remainder_near(1):
                    self._errors[field] = self.error_class(["Per questo prodotto usa quantità intere"])
                    del self.cleaned_data["quantity"]

class ProductForm(QuantityForm):
    class Meta:
        model = Product
        fields = ("name", "code", "category", "unit", "quantity", "min_quantity")

    def clean(self):
        cleaned_data = super(ProductForm, self).clean()
        self.check_integral_quantity(self.instance.product, ["quantity", "min_quantity"])
        return cleaned_data

class ProductExtraForm(ModelForm):

    class Meta:
        model = Product
        fields = ('catalogue', 'denominator')
        widgets = {
            'denominator': HiddenInput(),
        }

class IncomingProductForm(ModelForm):
    class Meta:
        model = IncomingProduct
        fields = ("quantity", "new_supplier_code", "new_supplier_price")

    def clean(self):
        cleaned_data = super(ProductForm, self).clean()
        self.check_integral_quantity(self.instance.actual_product, ["quantity"])
        return cleaned_data


class SupplyForm(ModelForm):
    class Meta:
        model = Supply
        fields = ("supplier", "code", "price", "altprice")

class ModifySupplyForm(ModelForm):
    class Meta:
        model = Supply
        fields = ("price", "altprice", "code")

class BatchSupplierForm(ModelForm):
	class Meta:
		model = BatchLoad
		fields = ("document_ref", "supplier")

class ModifyPriceForm(ModelForm):
    method = ChoiceField(required=True, label="Tipo di prezzo", choices=PRICE_MAKING_METHODS, initial="==", widget=RadioSelect)

    def clean(self):
        cleaned_data = self.cleaned_data
        method = cleaned_data.get("method")
        if not method:
            if self._errors.has_key("markup"):
                del(self._errors["markup"])
            if self._errors.has_key("gross"):
                del(self._errors["gross"])
        elif method == '==':
            if self._errors.has_key("markup"):
                del(self._errors["markup"])
        else:
            if self._errors.has_key("gross"):
                del(self._errors["gross"])
        return cleaned_data

    class Meta:
        model = AbstractPrice
        fields = ("method", "gross", "markup")

class ChildCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ("name",)

class CategoryForm(ModelForm):
    class Meta:
        model = Category
