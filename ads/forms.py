from django import forms

from ads.models import Ad, Category, User


class AdForm(forms.ModelForm):
    author = forms.CharField()
    category = forms.CharField()

    class Meta:
        model = Ad
        fields = ['name', 'price', 'description', 'is_published']

    def clean_category(self):
        category = self.data['category']
        if type(category) is str:
            category_obj, _ = Category.objects.get_or_create(name=category)
            return category_obj
        else:
            return category

    def clean_author(self):
        username = self.data['author']
        if type(username) is str:
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                return user
            else:
                print(1)
                raise forms.ValidationError('Unknown user')
        else:
            return username


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
