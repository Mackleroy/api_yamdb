from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Class of Category model"""
    name = models.TextField(max_length=32)
    slug = models.SlugField(unique=True, max_length=32)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Class of Genre model"""
    name = models.TextField(max_length=32)
    slug = models.SlugField(unique=True, max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Title(models.Model):
    """Class of Title model"""
    name = models.TextField(max_length=256)
    year = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='titles')
    genre = models.ManyToManyField(Genre, related_name='titles', blank=True,
                                   null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)

    def get_genres(self):
        return ', '.join([str(genre) for genre in self.genre.all()])

    class Meta:
        ordering = ['id']


class Review(models.Model):
    """Class of Review model"""
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']


class Comment(models.Model):
    """Class of Comment model"""
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
