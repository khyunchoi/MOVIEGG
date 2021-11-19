from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=30)


class Movie(models.Model):
    movie_code = models.IntegerField()
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    director = models.CharField(max_length=30)
    plot = models.TextField(default='')
    showtime = models.IntegerField()
    actors = models.CharField(default='', max_length=500)
    poster_path = models.TextField(default='')
    genre = models.ManyToManyField(Genre, related_name='movie_genre')


class BoxofficeMovie(models.Model):
    title = models.CharField(max_length=100)
    rank = models.IntegerField()
    rank_inten = models.IntegerField()


class Character(models.Model):
    name = models.CharField(max_length=20)
    number = models.IntegerField()
    genre = models.ManyToManyField(Genre, related_name='character_genre')


class Question(models.Model):
    content = models.CharField(max_length=100)