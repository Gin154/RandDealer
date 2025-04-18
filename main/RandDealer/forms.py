from django import forms
from .models import Cars, CarImage

class CarRegistrationForm(forms.ModelForm):
    class Meta:
        model = Cars
        fields = ['maker', 'model', 'year', 'mileage', 'price', 'condition', 'description']