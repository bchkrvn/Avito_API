from django.db import models
from authentication.models import User


class Category(models.Model):
    name = models.CharField(max_length=25)

    def __repr__(self):
        return f'Category({self.name})'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Ad(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.CharField(max_length=1000, null=False)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __repr__(self):
        return f'Ads({self.name})'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
