from django import forms

from django.contrib.auth.models import User
from .models import Profile, Item


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = Profile
        fields = ['avatar']
        
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        image_link = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
        fields = ['name', 'price', 'description', 'image_link', 'category']