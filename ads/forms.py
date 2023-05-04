from django.forms import ModelForm

from ads.models import Category


class CategoryForm(ModelForm):
    model = Category
    fields = ['name']
