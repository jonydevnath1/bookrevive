from django import forms
from .models import ShippingAddress, Product

class ShippingFrom(forms.ModelForm):
    shipping_full_name = forms.CharField(label="Full Name ", widget=forms.TextInput(attrs={'class': 'form-control mt-2', 'placeholder': ''}), required=True)
    shipping_phone = forms.CharField(label="Phone ", widget=forms.TextInput(attrs={'class': 'form-control mt-2', 'placeholder': ''}), required=True)
    shipping_email = forms.CharField(label="Email Address ", widget=forms.TextInput(attrs={'class': 'form-control mt-2', 'placeholder': ''}), required=True)
    shipping_address1 = forms.CharField(label="Address 1 ", widget=forms.TextInput(attrs={'class': 'form-control mt-2', 'placeholder': ''}), required=True)
    shipping_address2 = forms.CharField(label="Address 2 ", widget=forms.TextInput(attrs={'class': 'form-control mt-2', 'placeholder': ''}), required=True)
    shipping_city = forms.CharField(label="City ", widget=forms.TextInput(attrs={'class': 'form-control mt-2', 'placeholder': ''}), required=True)
    shipping_state = forms.CharField(label="State ", widget=forms.TextInput(attrs={'class': 'form-control mt-2', 'placeholder': ''}), required=False)
    shipping_zipcode = forms.CharField(label="Zip Code ", widget=forms.TextInput(attrs={'class': 'form-control mt-2', 'placeholder': ''}), required=False)
    shipping_country = forms.CharField(label="Country ", widget=forms.TextInput(attrs={'class': 'form-control mt-2', 'placeholder': ''}), required=True)
    payment_method = forms.CharField(label="COD | Bkash Or Nagad Trx ID", widget=forms.TextInput(attrs={'class': 'form-control mt-2', 'placeholder': ''}), required=True)

    class Meta:
        model = ShippingAddress
        fields = ('shipping_full_name', 'shipping_phone', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country', 'payment_method')

        exclude = ['user',]

class PaymentForm(forms.ModelForm):
    pass

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image', 'category', 'is_sale', 'sale_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mt-2', 'placeholder': 'Product Name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control mt-2', 'placeholder': 'Product Price'}),
            'description': forms.Textarea(attrs={'class': 'form-control mt-2', 'placeholder': 'Product Description', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control mt-2'}),
            'category': forms.Select(attrs={'class': 'form-control mt-2'}),
            'is_sale': forms.CheckboxInput(attrs={'class': 'form-check-input mt-2'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control mt-2', 'placeholder': 'Sale Price'}),
        }
