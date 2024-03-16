from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import User, Tweet, Like, Retweet, Comment
from .serializers import UserSerializer, TweetSerializer, LikeSerializer, RetweetSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from .forms import RegistrationForm, UserUpdateForm, TweetForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class RetweetViewSet(viewsets.ModelViewSet):
    queryset = Retweet.objects.all()
    serializer_class = RetweetSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class MyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm
    return render(request, 'registration/register.html', {"form": form})


@login_required
def profile(request):
    user = request.user
    return render(request, 'registration/profile.html', {'user': user})


@login_required
def settings(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Account updated')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
    return render(request, 'registration/settings.html', {'user_form': user_form})


def homepage(request):
    tweets = Tweet.objects.all()
    form = TweetForm()
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('homepage')
    return render(request, 'registration/homepage.html', {'tweets': tweets, 'form': form})


def like_tweet(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
    if not created:
        like.delete()
    return redirect('homepage')


def retweet_tweet(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    retweet, created = Retweet.objects.get_or_create(user=request.user, tweet=tweet)
    if not created:
        retweet.delete()
    return redirect('homepage')


def reply_to_tweet(request, tweet_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        tweet = Tweet.objects.get(id=tweet_id)
        user = request.user
        if content:
            Comment.objects.create(user=user, tweet=tweet, content=content)
            return redirect('homepage')
        else:
            return HttpResponseBadRequest("Invalid request")
    else:
        # Handle GET requests, render reply form
        return render(request, 'registration/reply_form.html')


def tweet_detail_view(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    replies = tweet.comment_set.all()
    return render(request, 'registration/tweet_detail.html', {'tweet': tweet, 'replies': replies})
