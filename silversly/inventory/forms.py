from django.forms import ModelForm, Form, BooleanField, ChoiceField, RadioSelect
from decimal import Decimal
from models import *

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ("name", "code", "category", "unit", "quantity", "min_quantity")

class IncomingProductForm(ModelForm):
    class Meta:
        model = IncomingProduct
        fields = ("quantity", "new_supplier_code", "new_supplier_price")

class SupplyForm(ModelForm):
    class Meta:
        model = Supply
        fields = ("supplier", "code", "price")

class ModifySupplyForm(ModelForm):
    class Meta:
        model = Supply
        fields = ("price", "code")

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
        model = Price
        fields = ("method", "gross", "markup")

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