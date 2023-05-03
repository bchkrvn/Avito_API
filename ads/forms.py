from django import forms

from ads.models import Ad, Category


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['name', 'author', 'price', 'description', 'is_published']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
