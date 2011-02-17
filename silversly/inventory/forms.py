from django.forms import ModelForm
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

class ModifyMarkupForm(ModelForm):
    class Meta:
        model = Markup
        fields = ("charge",)

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