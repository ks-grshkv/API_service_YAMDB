from enum import Enum, auto

from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(Enum):
    admin = 'admin'
    user = 'user'
    moderator = 'moderator'


class User(AbstractUser):
    CHOICES = (
        (Roles.admin.name, 'Администратор'),
        (Roles.user.name, 'Пользователь'),
        (Roles.moderator.name, 'Модератор'),
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=10,
        choices=CHOICES,
        default=Roles.user.name,
    )
    confirmation_code = models.CharField(
        max_length=5,
        default='00000',
    )
    password = models.CharField(max_length=10, blank=True)
