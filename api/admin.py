from django.contrib import admin

from api.models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'category', 'get_genres']
    list_filter = ['year', 'category', 'genre']
    search_fields = ['name']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'author', 'score', 'pub_date']
    list_filter = ['score', 'pub_date']
    search_fields = ['title', 'text', 'author']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['review', 'text', 'author', 'pub_date']
    list_filter = ['pub_date']
    search_fields = ['review', 'text', 'author']
