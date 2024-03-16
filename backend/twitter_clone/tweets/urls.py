from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TweetViewSet, LikeViewSet, RetweetViewSet, CommentViewSet, register, profile, settings
from . import views

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tweets', TweetViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'retweets', RetweetViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('settings/', settings, name='settings'),
    path('like/<int:tweet_id>/', views.like_tweet, name='like_tweet'),
    path('retweet/<int:tweet_id>/', views.retweet_tweet, name='retweet_tweet'),
    path('reply/<int:tweet_id>/', views.reply_to_tweet, name='reply_to_tweet'),
    path('tweet/<int:tweet_id>/', views.tweet_detail_view, name='tweet_detail'),
]
