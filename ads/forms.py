from django import forms

from ads.models import Category, User


class AdCreateForm(forms.Form):
    category = forms.CharField()
    name = forms.CharField(max_length=50)
    author = forms.CharField()
    price = forms.IntegerField()
    description = forms.CharField(max_length=1000)
    is_published = forms.BooleanField()

    def clean_category(self):
        category = self.data['category']
        category_obj, _ = Category.objects.get_or_create(name=category)
        return category_obj

    def clean_author(self):
        username = self.data['author']
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            return user
        else:
            raise forms.ValidationError('Unknown user')


class AdUpdateForm(forms.Form):
    category = forms.CharField(required=False)
    name = forms.CharField(required=False)
    price = forms.IntegerField(required=False)
    description = forms.CharField(required=False)
    is_published = forms.BooleanField(required=False)

    def clean_category(self):
        category = self.data.get('category', None)
        if not category:
            return None
        category_obj, _ = Category.objects.get_or_create(name=category)
        return category_obj

    def clean_name(self):
        name = self.data.get('name', None)
        if not name:
            return None
        else:
            return name

    def clean_price(self):
        price = self.data.get('price', None)
        if not price:
            return None
        if type(price) is int or price.isdigit():
            return price
        else:
            raise forms.ValidationError('wrong price')

    def clean_description(self):
        description = self.data.get('description', None)
        if not description:
            return None
        else:
            return description

    def clean_is_published(self):
        is_published = self.data.get('is_published', None)
        if not is_published:
            return None
        elif not type(is_published) is bool:
            raise forms.ValidationError('wrong is_published')
        else:
            return is_published


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
