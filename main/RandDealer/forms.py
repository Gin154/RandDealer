from django import forms
from .models import Cars, CarImage, UserProfile
from django.contrib.auth.models import User

class CarRegistrationForm(forms.ModelForm):
    class Meta:
        model = Cars
        fields = ['maker', 'model', 'year', 'mileage', 'price', 'condition', 'description']

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

class AddUserInfo(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']