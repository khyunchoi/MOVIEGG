from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('<int:movie_pk>/movie_detail/', views.movie_detail, name='movie_detail'),

    path('load/', views.load),
    path('movieupdate/', views.movieupdate),
    path('genreupdate/', views.genreupdate),
]
