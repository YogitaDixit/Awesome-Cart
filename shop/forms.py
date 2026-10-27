from django import forms
from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "address_title",
            "full_name",
            "phone",
            "address_line1",
            "address_line2",
            "city",
            "state",
            "zip_code",
        ]