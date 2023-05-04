from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=25)

    def json(self):
        return {'name': self.name}

    def __repr__(self):
        return f'Category({self.name})'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Location(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()

    def json(self):
        return {"name": self.name, 'lat': self.lat, 'lng': self.lng}

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return f'Location({self.name})'


class User(models.Model):
    ROLES = [
        ('member', 'Участник',),
        ('moderator', 'Модератор'),
        ('admin', "Админ")
    ]
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20, null=False, unique=True)
    password = models.CharField(max_length=20, null=False)
    role = models.CharField(max_length=10, choices=ROLES)
    age = models.IntegerField()
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE, default='member')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def json_short(self):
        return {'first_name': self.first_name, 'last_name': self.last_name, 'username': self.username}

    def __str__(self):
        return f'User({self.username})'


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class Ad(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.CharField(max_length=1000, null=False)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    published = PublishedManager()

    def json_full(self):
        return {'id': self.id, 'name': self.name, 'author': self.author.id, 'price': self.price,
                'description': self.description, 'is_published': self.is_published}

    def json_short(self):
        return {'id': self.id, 'name': self.name, 'author_id': self.author_id, 'price': self.price,
                'category_id': self.category_id, 'image': self.image.url if self.image else None}

    def __repr__(self):
        return f'Ads({self.name})'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
