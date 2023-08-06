from .feed import LatestPostsFeed
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('rss/', LatestPostsFeed(), name="post_feed"),
    path('<slug:slug>/', views.view_post, name='view_post'),
]
