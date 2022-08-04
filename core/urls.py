from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.index , name="home"),
    path('', views.index , name="home"),
    path('settings/', views.settings , name="settings"),
    path('profile/<str:pk>', views.profile , name="profile"),
    path('follow', views.follow , name="follow"),
    path('upload/', views.upload , name="upload"),
    path('like-post', views.like_post , name="like-post"),
    path('signup/', views.signup , name="signup"),
    path('login/', views.login , name="login"),
    path('logout/', views.logout , name="logout"),
    
]