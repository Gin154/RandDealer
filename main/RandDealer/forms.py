from django import forms
from .models import Cars, CarImage
from django.forms.models import inlineformset_factory

class CarRegistrationForm(forms.ModelForm):
    class Meta:
        model = Cars
        fields = ['maker', 'model', 'year', 'mileage', 'price', 'condition', 'description']