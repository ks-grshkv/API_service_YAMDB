from random import randrange

from django.contrib.auth.models import AbstractUser
from django.db import models

class Roles():
    admin = 'admin'
    user = 'user'
    moderator = 'moderator'

class User(AbstractUser):
    CHOICES = (
    	(Roles.user, 'Администратор'),
        (Roles.admin, 'Пользователь'),
        (Roles.moderator, 'Модератор'),
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
    confirmation_code = models.CharField(
        max_length=5,
        default='00000'
    )
    password = models.CharField(max_length=10, blank=True)

    def get_confirmation_code(self):
        self.confirmation_code = randrange(10000, 100000)
        return self.confirmation_code
