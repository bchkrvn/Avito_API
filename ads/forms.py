from django import forms

from ads.models import ADS, Category


class AdForm(forms.ModelForm):
    class Meta:
        model = ADS
        fields = ['name', 'author', 'price', 'description', 'address', 'is_published']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
