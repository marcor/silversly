from django.forms import ModelForm, Form, BooleanField, ChoiceField, RadioSelect
from decimal import Decimal
from inventory.models import Pricelist

class EditPricelistForm(ModelForm):
    class Meta:
        model = Pricelist
        fields = ("default_method", "default_markup")