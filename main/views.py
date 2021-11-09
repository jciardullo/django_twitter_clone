from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Tweet, Comment, Profile
from datetime import datetime

def main_view(request):
    if not request.user.is_authenticated:
        return redirect('/splash')
    if request.method == 'POST' and request.POST['body'] != "":
        tweet = Tweet.objects.create(
            body = request.POST['body'],
            author = request.user,
            created_at = datetime.now()
        )
        tweet.save()
    tweets = Tweet.objects.all().order_by('-created_at')
    comments = Comment.objects.all().order_by('created_at')
    return render(request, 'main.html', {'tweets': tweets, 'comments': comments})

def splash_view(request):
    return render(request, 'splash.html' )

def profile_view(request):
    user_profile = Profile.objects.get(user=request.GET['id'])
    if request.method == 'POST' and request.POST['body'] != "":
        user_profile.bio = request.POST['body']
        user_profile.save()
    user_tweets = Tweet.objects.all().filter(author=request.GET['id']).order_by('-created_at')
    num_tweets = len(user_tweets)
    user_tweet_comments = Comment.objects.all().filter(tweet__in=user_tweets).order_by('created_at')
    return render(request, 'profile.html' , {'user_profile': user_profile, 'tweets': user_tweets, 'num_tweets': num_tweets, 'comments': user_tweet_comments})

def login_view(request):
    username, password = request.POST['username'], request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return redirect('/splash?error=LoginError')

def signup_view(request):
    user = User.objects.create_user(
        username=request.POST['username'],
        password=request.POST['password'],
        email=request.POST['email'],
    )
    Profile.objects.create_user(
        user=user
    )
    login(request, user)
    return redirect('/')

def delete_view(request):
    if request.GET['type'] == "tweet":
        tweet = Tweet.objects.get(id=request.GET['id'])
        replies = Comment.objects.filter(tweet=tweet)
        if tweet.author == request.user:
            tweet.delete()
            for reply in replies:
                reply.delete()
    elif request.GET['type'] == "comment":
        comment = Comment.objects.get(id=request.GET['id'])
        if comment.author == request.user:
            comment.delete()

    return redirect(request.GET['path'])

def like_view(request):
    if request.GET['type'] == "tweet":
        tweet = Tweet.objects.get(id=request.GET['id'])
        if len(tweet.likes.filter(username=request.user.username)) == 0:
            tweet.likes.add(request.user)
        else:
            tweet.likes.remove(request.user)
        tweet.save()
    elif request.GET['type'] == "comment":
        comment = Comment.objects.get(id=request.GET['id'])
        if len(comment.likes.filter(username=request.user.username)) == 0:
            comment.likes.add(request.user)
        else:
            comment.likes.remove(request.user)
        comment.save()

    return redirect(request.GET['path'])

def comment_view(request):
    if request.method == 'POST' and request.POST['body'] != "":
        comment = Comment.objects.create(
            body = request.POST['body'],
            author = request.user,
            created_at = datetime.now(),
            tweet = Tweet.objects.get(id=request.GET['tweet_id'])
        )
        comment.save()
    return redirect('/')

def logout_view(request):
    logout(request)
    return redirect('/splash')