from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles():
    admin = 'admin'
    user = 'user'
    moderator = 'moderator'


class User(AbstractUser):
    CHOICES = (
        (Roles.admin, 'Администратор'),
        (Roles.user, 'Пользователь'),
        (Roles.moderator, 'Модератор'),
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=10,
        choices=CHOICES,
        default=Roles.user,
    )
    confirmation_code = models.CharField(
        max_length=5,
        default='00000',
        blank=False,
    )
