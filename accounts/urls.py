from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update, name='update'),
    path('password/', views.password_change, name='password_change'),
    # path('<int:user_pk>/', views.profile, name='profile'),
    path('practice/', views.practice, name="practice"),
]