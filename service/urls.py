# urls.py

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('bloggenerate/', views.generateBlog, name='generateBlog'),
    path('bloggenerate/getBlog/', views.getBlog, name='getBlog'),
    path('getBlog/', views.getBlog, name='getBlog'),
    path('userQuery/', views.user_query, name='userQuery'),
    path('update-like-dislike/<str:blog_title>/', views.update_like_dislike, name='update_like_dislike')
]
