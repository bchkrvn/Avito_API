from django.db import models
from django.contrib.auth.models import AbstractUser


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return f'Location({self.name})'


class User(AbstractUser):
    ROLES = [
        ('member', 'Участник',),
        ('moderator', 'Модератор'),
        ('admin', "Админ")
    ]

    role = models.CharField(max_length=10, choices=ROLES, default='member')
    age = models.IntegerField(blank=True, null=True)
    locations = models.ManyToManyField("Location")

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    # def save(self, *args, **kwargs):
    #     self.set_password(self.password)
    #     super().save()

    def __str__(self):
        return f'User({self.username})'
