from django.contrib.auth.models import AbstractUser
from django.db import models

class Roles():
    admin = 'admin'
    user = 'user'
    moderator = 'moderator'

class User(AbstractUser):
    CHOICES = (
        (Roles.admin, 'Пользователь'),
        (Roles.user, 'Администратор'),
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
        blank=True
    )
    password = models.CharField(max_length=10, blank=True)
    # username = models.CharField(max_length=40, unique=True)
    # USERNAME_FIELD = 'username'
    email = models.CharField(max_length=40, unique=True)
    EMAIL_FIELD = 'email'
    # REQUIRED_FIELDS = ['username','email']
