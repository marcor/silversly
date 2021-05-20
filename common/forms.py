from django.forms import ModelForm, Form, BooleanField, ChoiceField, RadioSelect
from decimal import Decimal
from inventory.models import Pricelist
from models import *

class EditPricelistForm(ModelForm):
    class Meta:
        model = Pricelist
        fields = ("default_method", "default_markup")

class OtherSettingsForm(ModelForm):
    class Meta:
        model = Settings
        exclude = ("site",)

class ShopForm(ModelForm):
    class Meta:
        model = Shop
        exclude = ("site",)
