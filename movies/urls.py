from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('load/', views.load),
    path('movieupdate/', views.movieupdate),
    path('genreupdate/', views.genreupdate),
]
