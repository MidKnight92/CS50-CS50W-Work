from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from .models import User, Post, Follower, Like


def index(request):
    # User made a post request
    if request.method == "POST":

        # Attempt to save post and direct user to all post
        try:
            # Get post text
            text = request.POST["post"]

            # Get the user
            user = request.user

            print(user)

            # Instiante a posts
            posts = Post(user=user, post=text)

            # Save posts to db
            posts.save()

            # Instiante a like
            like = Like(post=posts)

            # Save like to db
            like.save()
            return HttpResponseRedirect("posts")
        except expression as identifier:
            return HttpResponseRedirect(reverse("index"))  

    # User made a get request
    else:
        return render(request, "network/index.html", {
            "now": timezone.now()
        })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            Follower(followee=user)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def posts(request):
    try:
        # Query for most recent posts
        posts = Post.objects.all().order_by('-timestamp')

        # Get Like Count
        likes = Like.objects.all().order_by('post')
        # for like in likes:
        #     print(like)
        
        return render(request, "network/posts.html", {
            "posts": posts,
            "likes": 0
        })
    except expression as identifier:
    
        return HttpResponse("error")

def profile(request, username):
    
    # Get ID of user whose profile was selected
    username_profile = User.objects.filter(username=username).values_list('id', flat=True).first()

    # Get ID of current user
    current_user = request.user.id

    # User made a get request display profile of username
    if request.method == "GET":

        # Get all posts by user display latest post first
        posts = Post.objects.order_by('-timestamp').filter(user=username_profile)

        # print(posts)

        # Get profile users follower count
        followers = Follower.objects.filter(followee=username_profile).count()

        print(followers)

        # Get profile user count of users they are following
        following = Follower.objects.filter(user=username_profile).count()
        
        # Get List of users the current user is following
        followee = Follower.objects.filter(user=current_user, followee=username_profile)
        
        print("this is followee", followee)
        
        # Default current user is not following user
        following_user = False

        # Check if current user is following this user's profile
        if followee:
            following_user = True


        return render(request, "network/profile.html", {
            "profile_name": username,
            "posts": posts,
            "followers": followers,
            "following": following,
            "followee": following_user
        })

    # User made a post request (follow/unfollow username profile) 
    else:

        # Check if name value is follow else it's unfollow
        action = 'follow' if request.POST.get('follow') else 'unfollow'
        
        # Follow user save to Follower db
        if action == 'follow':
            follow = Follower(user=request.user, followee=User.objects.get(username=username))
            follow.save()
        else:
            # Get query of current user and profile user
            queryset = Follower.objects.filter(user=current_user, followee=username_profile)

            # Delete from Follower db
            queryset.delete()

        return HttpResponseRedirect(f"{username}")