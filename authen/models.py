from django.contrib.auth.models import AbstractUser
from django.db import models
from config.settings import NULLABLE


class Country(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    description = models.CharField(max_length=30, verbose_name='Описание')

    class Meta:
        verbose_name = 'страна'
        verbose_name_plural = 'страны'

    def __str__(self):
        return self.description


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='почта', unique=True)
    phone = models.CharField(verbose_name='телефон', unique=True, max_length=20, **NULLABLE)
    avatar = models.ImageField(verbose_name='аватар', upload_to='img/user', **NULLABLE)
    token = models.CharField(verbose_name="Токен", **NULLABLE, max_length=100)

    country = models.ForeignKey(
        to=Country,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name='страна',
        ** NULLABLE
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('first_name', 'last_name', 'email')

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.email
