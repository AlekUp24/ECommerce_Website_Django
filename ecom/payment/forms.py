from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}), required=True)
    shipping_email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=True)
    shipping_address1 = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 1'}), required=True)
    shipping_address2 = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 2'}), required=True)
    shipping_city = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=True)
    shipping_state= forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}), required=False)
    shipping_zipcode = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'ZIP Code'}), required=False)
    shipping_country = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}), required=True)

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name',
                  'shipping_email',
                  'shipping_address1',
                  'shipping_address2',
                  'shipping_ciy',
                  'shipping_state',
                  'shipping_zipcode',
                  'shipping_country',
                  ]
        exclude = ['user',]
