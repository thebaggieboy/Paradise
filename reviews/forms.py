from django import forms
from .models import Reviews
class ReveiwForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['review']
