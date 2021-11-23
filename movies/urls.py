from django.urls import path,include
from . import views

app_name = 'movies'
urlpatterns = [
    path('<int:movie_pk>/movie_detail/', views.movie_detail, name='movie_detail'),

    path('load/', views.load),
    path('movieupdate/', views.movieupdate),
    path('genreupdate/', views.genreupdate),
    path('lolupdate/', views.leagueoflegend),
    path('lol_recommend/', views.lol_recommend ,name="lol_recommend"),
    path('lol_reccomend_start/', views.lol_reccomend_start, name="lol_reccomend_start"),
    path('lolresult/<int:i>', views.lol_result, name="lol_result")
]
