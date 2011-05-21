from models import *
from django.forms import ModelForm

class SellProductForm(ModelForm):
    class Meta:
        model = CartItem
        fields = ("quantity", "discount", "update")

class EditDiscountForm(ModelForm):
    class Meta:
        model = Cart
        fields = ("discount",)

class ReceiptForm(ModelForm):
    class Meta:
        model = Scontrino
        fields = ("payed",)
