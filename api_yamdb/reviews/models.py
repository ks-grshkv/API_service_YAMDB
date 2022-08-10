from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Title(models.Model):
    name = models.TextField(max_length=50)
    year = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT,
        related_name="titles", blank=True, null=True
    )

    genres = models.ManyToManyField(Genre, through='GenreTitle')

    def __str__(self):
        return self.name

class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}' 