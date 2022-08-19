from enum import Enum

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
        blank=False,
    )

    @property
    def is_admin(self):
        return self.role == Roles.admin.name

    @property
    def is_user(self):
        return self.role == Roles.user.name

    @property
    def is_moderator(self):
        return self.role == Roles.moderator.name

