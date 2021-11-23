from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update, name='update'),
    path('password/', views.password_change, name='password_change'),
    path('<int:user_pk>/profile_review/', views.profile_review, name='profile_review'),
    path('<int:user_pk>/profile_freeboard/', views.profile_freeboard, name='profile_freeboard'),
    path('practice/', views.practice, name="practice"),
]
