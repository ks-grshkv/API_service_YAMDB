from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

class Title(models.Model):
    name = models.TextField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="titles")

    genre = models.ManyToManyField(Genre, through='GenreTitle')

    def __str__(self):
        return self.name

class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}' 


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review'
    )
    text = models.TextField()
    #score =
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True
    )
