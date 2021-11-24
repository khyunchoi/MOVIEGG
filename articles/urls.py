from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    # 메인 페이지
    path('', views.index, name='index'),

    # 검색 페이지
    path('search/', views.search, name='search'),
    path('search/movie', views.search_movie, name='search_movie'),

    # 리뷰 게시판
    path('review/', views.review, name='review'),
    path('<int:movie_pk>/review_create/', views.review_create, name='review_create'),
    path('<int:review_pk>/review_detail/', views.review_detail, name='review_detail'),
    path('<int:review_pk>/review_update/', views.review_update, name='review_update'),
    path('<int:review_pk>/review_delete/', views.review_delete, name='review_delete'),
    path('<int:review_pk>/review_like/', views.review_like, name='review_like'),
    path('<int:review_pk>/review_detail/comment_create', views.review_comment_create, name='review_comment_create'),
    path('<int:review_pk>/review_detail/<int:comment_pk>/comment_delete', views.review_comment_delete, name='review_comment_delete'),

    #자유 게시판
    path('freeboard/', views.freeboard, name='freeboard'),
    path('freeboard_create/', views.freeboard_create, name='freeboard_create'),
    path('<int:freeboard_pk>/freeboard_detail/', views.freeboard_detail, name='freeboard_detail'),
    path('<int:freeboard_pk>/freeboard_update/', views.freeboard_update, name='freeboard_update'),
    path('<int:freeboard_pk>/freeboard_delete/', views.freeboard_delete, name='freeboard_delete'),
    path('<int:freeboard_pk>/freeboard_like/', views.freeboard_like, name='freeboard_like'),
    path('<int:freeboard_pk>/freeboard_detail/comment_create', views.free_comment_create, name='free_comment_create'),
    path('<int:freeboard_pk>/freeboard_detail/<int:comment_pk>/comment_delete', views.free_comment_delete, name='free_comment_delete'),
]
