from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title

@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category', 'rating')
    empty_value_display = '-пусто-'

@admin.register(Category, Genre, Review, Comment)
class ReviewAdmin(admin.ModelAdmin):
    pass