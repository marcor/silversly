from django.forms import ModelForm
from models import *

class SupplierForm(ModelForm):
    class Meta:
        model = Supplier

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ("name", "code", "phone", "email", "payment_method", "bank", "costs")