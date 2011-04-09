from models import *
from django.forms import ModelForm

class CartItemForm(ModelForm):
    class Meta:
        model = CartItem
        fields = ("quantity", "discount", "update")