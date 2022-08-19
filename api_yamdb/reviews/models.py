from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Категория',
        help_text='Область искусства (например: Музыка, Книги)'
    )
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Жанр',
        help_text='Например: Сказка, Рок, Артхаус'
    )
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(
        max_length=256,
        db_index=True,
        verbose_name='Произведение',
        help_text='Например: Понедельник начинается в субботу'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год публикации',
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
    )

    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )

    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='GenreTitle',
        through_fields=('title', 'genre')
    )

    filter_horizontal = ('category', 'genre',)

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
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='review',
        db_index=True
    )
    text = models.TextField(verbose_name='Отзыв на произведение')
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка произведения',
        help_text='Оцените произведение от 1 до 10',
        validators=[
            MinValueValidator(
                1, message='Баллы должны быть в диапазоне от 1 до 10'
            ),
            MaxValueValidator(
                10, message='Баллы должны быть в диапазоне от 1 до 10'
            )
        ],
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
        related_name='review'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = (
            UniqueConstraint(fields=['author', 'title'],
                             name='unique_review'),
        )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(verbose_name='Комментарий к отзыву')
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
