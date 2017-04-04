from django.forms import *
from models import *
import re

ADDRESS_FORMAT = getattr(settings, 'ADDRESS_FORMAT')

class SupplierForm(ModelForm):
    class Meta:
        model = Supplier

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ("name", "cf", "phone", "email")

class CustomerInfoForm(ModelForm):
    class Meta:
        model = Customer
        fields = ("name", "cf", "phone", "email")

class CustomerQuickForm(ModelForm):
    class Meta:
        model = Customer
        fields = ("name", "cf", "pricelist", "discount")

class CompanyForm(ModelForm):
    class Meta:
        model = CompanyCustomer
        fields = ("name", "piva", "main_address", "phone", "email")

    def clean_main_address(self):
        address = self.cleaned_data['main_address'].strip()
        if not re.match(ADDRESS_FORMAT, address):
            raise ValidationError("L'indirizzo e' incompleto o non rispetta il formato corretto.")
        return address

class PAForm(CompanyForm):
    class Meta(CompanyForm.Meta):
        model = PACustomer
        fields = ("name", "piva", "cu", "main_address", "phone", "email")

class CompanyInfoForm(ModelForm):
    class Meta:
        model = CompanyCustomer
        fields = ("name", "cf", "piva", "phone", "email", "main_address")

    def clean_main_address(self):
        address = self.cleaned_data['main_address'].strip()
        if not re.match(ADDRESS_FORMAT, address):
            raise ValidationError("L'indirizzo e' incompleto o non rispetta il formato corretto.")
        return address

class PAInfoForm(CompanyInfoForm):
    class Meta:
        model = PACustomer
        fields = ("name", "cf", "piva", "cu", "phone", "email", "main_address")

class CompanyCommercialForm(ModelForm):
    class Meta:
        model = CompanyCustomer
        fields = ("due", "pricelist", "discount", "payment_method", "shipping_address")

class CompanyQuickForm(ModelForm):
    class Meta:
        model = CompanyCustomer
        fields = ("name", "piva", "pricelist", "discount", "main_address")

    def clean_main_address(self):
        address = self.cleaned_data['main_address'].strip()
        if not re.match(ADDRESS_FORMAT, address):
            raise ValidationError("L'indirizzo e' incompleto o non rispetta il formato corretto.")
        return address

class PAQuickForm(CompanyQuickForm):
    class Meta:
        model = PACustomer
        fields = ("name", "piva", "cu", "pricelist", "discount", "main_address")

    def clean_main_address(self):
        address = self.cleaned_data['main_address'].strip()
        if not re.match(ADDRESS_FORMAT, address):
            raise ValidationError("L'indirizzo e' incompleto o non rispetta il formato corretto.")
        return address

class CustomerCommercialForm(ModelForm):
    class Meta:
        model = Customer
        fields = ("due", "pricelist", "discount")

