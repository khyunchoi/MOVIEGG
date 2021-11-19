from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=30)
    genre_num = models.IntegerField()
    


class Movie(models.Model):
    movie_code = models.IntegerField(null=True)
    title = models.CharField(max_length=100,null=True)
    release_date = models.DateField(null=True)
    director = models.CharField(max_length=30, null=True)
    plot = models.TextField(default='')
    showtime = models.IntegerField(null=True)
    poster_path = models.TextField(default='', null=True)
    genre = models.ManyToManyField(Genre, related_name='movie_genre',null=True)

class Actor(models.Model):
    movie_code = models.ManyToManyField(Movie, related_name='movie_actor')
    name = models.CharField(max_length=50)


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