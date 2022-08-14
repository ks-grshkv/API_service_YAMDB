from django.contrib import admin

from .models import Category, Genre, GenreTitle, Title, Review, Comment


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category', 'rating')
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(GenreTitle)
admin.site.register(Review)
admin.site.register(Comment)
