from django.forms import *
from models import *
import re
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.utils.safestring import mark_safe


ADDRESS_FORMAT = getattr(settings, 'ADDRESS_FORMAT')

class BankWidget(MultiWidget):
    def __init__(self, attrs=None):
        widgets = (TextInput(attrs=attrs),
                   TextInput(attrs=attrs))
        super(BankWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            bank = Bank.objects.get(pk=value)
            return [bank.abi, bank.cab]
        return [None, None]

    def format_output(self, rendered_widgets):
        # hack
        rendered_widgets.insert(1, '\n</p>\n<p><label for="id_bank_1">CAB:</label>')
        return u''.join(rendered_widgets)

class BankSplitField(MultiValueField):
    widget = BankWidget
    default_error_messages = {
        'invalid_abi': _(u'ABI non valido.'),
        'invalid_cab': _(u'CAB non valido.'),
    }

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        fields = (
            CharField(label="ABI", max_length=5, min_length=5, error_messages={'invalid': errors['invalid_abi']}),
            CharField(label="CAB", max_length=5, min_length=5, error_messages={'invalid': errors['invalid_cab']}))
        super(BankSplitField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            # Raise a validation error if time or date is empty
            # (possible if SplitDateTimeField has required=False).
            if data_list[0] in validators.EMPTY_VALUES:
                raise ValidationError(self.error_messages['invalid_abi'])
            if data_list[1] in validators.EMPTY_VALUES:
                raise ValidationError(self.error_messages['invalid_cab'])
            try:
                result = Bank.objects.get(abi=data_list[0], cab=data_list[1])
            except:
                result = Bank.objects.create(abi=data_list[0], cab=data_list[1])
            return result
        return None

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
        fields = ("name", "piva", "sdi_code", "main_address", "phone", "email")

    def clean_main_address(self):
        address = self.cleaned_data['main_address'].strip()
        if not re.match(ADDRESS_FORMAT, address):
            raise ValidationError("L'indirizzo e' incompleto o non rispetta il formato corretto.")
        return address

class PAForm(CompanyForm):
    class Meta(CompanyForm.Meta):
        model = PACustomer
        fields = ("name", "piva", "sdi_code", "main_address", "phone", "email")

class CompanyInfoForm(ModelForm):
    class Meta:
        model = CompanyCustomer
        fields = ("name", "cf", "piva", "sdi_code", "phone", "email", "main_address")

    def clean_main_address(self):
        address = self.cleaned_data['main_address'].strip()
        if not re.match(ADDRESS_FORMAT, address):
            raise ValidationError("L'indirizzo e' incompleto o non rispetta il formato corretto.")
        return address

class PAInfoForm(CompanyInfoForm):
    class Meta:
        model = PACustomer
        fields = ("name", "cf", "piva", "sdi_code", "phone", "email", "main_address")

class CompanyCommercialForm(ModelForm):
    bank = BankSplitField(label="ABI", required=False)  # hack

    class Meta:
        model = CompanyCustomer
        fields = ("due", "pricelist", "discount", "payment_method", "bank", "shipping_address")

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
        fields = ("name", "piva", "sdi_code", "pricelist", "discount", "main_address")

    def clean_main_address(self):
        address = self.cleaned_data['main_address'].strip()
        if not re.match(ADDRESS_FORMAT, address):
            raise ValidationError("L'indirizzo e' incompleto o non rispetta il formato corretto.")
        return address

class CustomerCommercialForm(ModelForm):
    class Meta:
        model = Customer
        fields = ("due", "pricelist", "discount")

