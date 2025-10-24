from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'placeholder': 'Enter amount'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Payment description'
            }),
        }
