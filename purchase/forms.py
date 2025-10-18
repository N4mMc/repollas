from django import forms
from .models import Purchase

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'  # o puedes listar solo algunos campos si prefieres
