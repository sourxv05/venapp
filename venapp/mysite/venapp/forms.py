from django import forms
from .models import profile

class profileform(forms.ModelForm):
    class Meta:
        model=profile
        fields=['name','address','phone','email']

