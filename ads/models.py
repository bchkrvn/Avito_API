from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=25)

    def json(self):
        return {'id': self.id, 'name': self.name}

    def __repr__(self):
        return f'Category({self.name})'


class ADS(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=20)
    price = models.IntegerField()
    description = models.CharField(max_length=1000, null=False)
    address = models.CharField(max_length=100, null=False)
    is_published = models.BooleanField(default=False)

    def json_full(self):
        return {'id': self.id, 'name': self.name, 'author': self.author, 'price': self.price,
                'description': self.description, 'address': self.address, 'is_published': self.is_published}

    def json_short(self):
        return {'id': self.id, 'name': self.name, 'author': self.author, 'price': self.price}

    def __repr__(self):
        return f'ADS({self.name})'
