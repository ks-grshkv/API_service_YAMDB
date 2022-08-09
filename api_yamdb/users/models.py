from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CHOICES = (
        ('admin', 'Администратор'),
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=10,
        choices=CHOICES,
        default=CHOICES[0],
    )
