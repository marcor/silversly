from django.forms import ModelForm, Form, BooleanField, ChoiceField, RadioSelect
from decimal import Decimal
from models import *

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ("name", "code", "category", "unit", "quantity", "min_quantity")

class SupplyForm(ModelForm):
    class Meta:
        model = Supply
        fields = ("supplier", "code", "price")

class ModifySupplyForm(ModelForm):
    class Meta:
        model = Supply
        fields = ("price", "code")


class SupplierForm(ModelForm):
    class Meta:
        model = Supplier

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ("name", "code", "phone", "email", "payment_method", "bank", "costs")

class MainAddressForm(ModelForm):
    class Meta: 
        model = Address

class ModifyPriceForm(ModelForm):
    method = ChoiceField(required=True, label="Tipo di prezzo", choices=PRICE_MAKING_METHODS, initial="==", widget=RadioSelect)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        method = cleaned_data.get("method")
        if not method:
            if self._errors.has_key("markup"):
                del(self._errors["markup"])
            if self._errors.has_key("value"):
                del(self._errors["value"])
        elif method == '==':
            if self._errors.has_key("markup"):
                del(self._errors["markup"])
        else:
            if self._errors.has_key("value"):
                del(self._errors["value"])
        return cleaned_data
            
    class Meta:
        model = Price
        fields = ("method", "value", "markup")

class ChildCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ("name",)

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        
class CartItemForm(ModelForm):
    class Meta:
        model = CartItem
        fields = ("quantity", "discount", "update")