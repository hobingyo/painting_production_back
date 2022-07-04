"""ppb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from article import views

from rest_framework import routers
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    #article/
    path('', views.ArticleView.as_view()),
    path('article/', views.ArticleView.as_view()),
    path('all/', views.AllArticleView.as_view()),
    path('comment/<comment_id>/', views.CommentView.as_view()),
    path('comment/<comment_id>/username', views.CommentUserView.as_view()),
    path('commenting/<article_id>/', views.CommentView.as_view()),
    path('<obj_id>/update/', views.ArticleView.as_view()),
    path('<obj_id>/delete/', views.ArticleView.as_view()),
    path('<obj_id>/', views.ArticleDetailView.as_view()),
    path('<obj_id>/username/', views.ArticleUserView.as_view()),
    
]