from django.contrib import admin
from .models import Genre, Movie, Actor, BoxofficeMovie, Character, Question

# Register your models here.
admin.site.register([Genre, Movie, Actor, BoxofficeMovie, Character, Question])