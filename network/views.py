from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import JsonResponse
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, Post, Follower, Like
from sqlalchemy.sql import expression


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


@csrf_exempt
def posts(request):
    if request.method == "GET":
        try:
            # Query for most recent posts
            posts = Post.objects.all().order_by('-timestamp')

            paginator = Paginator(posts, 10)

            page = request.GET.get('page')
            page_obj = paginator.get_page(page)

            try:
                # Page is not the first or last
                posts = paginator.page(page_obj)
            except PageNotAnInteger:
                # First page
                posts = paginator.page(1)
            except EmptyPage:
                # Last Page
                posts = paginator.page(paginator.num_pages)
            
            
            # like = Like.objects.filter(user=request.user.id).order_by('-post').values('post')
            # print("This is like",like)

            liked_by_user = []

            liked = False
            for p in posts:
                if Like.objects.filter(user=request.user.id, post=p.id):
                    liked = True
                liked_by_user.append(liked)


            likes = []
            for p in posts:
                # print(p)
                p_id = p.id
                li = Like.objects.filter(post=p_id)
                if not li:
                    li = 0
                else:
                   li = li.count()
                # print("this is li", li)
                likes.append(li)

            print(liked_by_user)
           
            return render(request, "network/posts.html", {
                "page": page_obj,
                "posts": posts,
                "likes": likes,
                "like": liked_by_user
            })
        except expression as identifier:
            return HttpResponse("error")
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            post = Post.objects.filter(pk=data['post_id']).update(post=data['post'])
            return HttpResponse("success")
        except expression as identifier:
            return HttpResponse("error")
    else:
        try:
            print("in put of the posts")

            data = json.loads(request.body)
            print("this data\n",data)
            post_instance = Post.objects.filter(pk=data['post_id'])
            print("this is the post_instance\n",post_instance)

            user_instance = User.objects.filter(pk=data['user_id'])
            print("this is the user_instance\n", user_instance)

            like = Like.objects.filter(post=data['post_id'], user=data['user_id'])
            
            print("this is the like\n",like)
            
            if not like:
                print("new like")
                like = Like(post=post_instance[0], user=user_instance[0])
                like.save()
            else:
                print('delete')
                like.delete()
            return HttpResponse("success")
        except expression as identifier:
            return HttpResponse("error")
        
        

@login_required
@csrf_exempt
def profile(request, username):
    
    # Get ID of user whose profile was selected
    username_profile = User.objects.filter(username=username).values_list('id', flat=True).first()

    # Get ID of current user
    current_user = request.user.id

    # User made a get request display profile of username
    if request.method == "GET":

        # Get all posts by user display latest post first
        posts_list = Post.objects.order_by('-timestamp').filter(user=username_profile)

        paginator = Paginator(posts_list, 10)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        
        try:
            # Page is not the first or last
            posts = paginator.page(page_obj)
        except PageNotAnInteger:
            # First page
            posts = paginator.page(1)
        except EmptyPage:
            # Last Page
            posts = paginator.page(paginator.num_pages)

        # Get profile users follower count
        followers = Follower.objects.filter(followee=username_profile).count()


        # Get profile user count of users they are following
        following = Follower.objects.filter(user=username_profile).count()
        
        # Query db for user following this profile user
        followee = Follower.objects.filter(user=current_user, followee=username_profile)
        

        # Default current user is not following user
        following_user = False

        # Check if current user is following this user's profile
        if followee:
            following_user = True


        return render(request, "network/profile.html", {
            "page": page_obj,
            "profile_name": username,
            "posts": posts,
            "followers": followers,
            "following": following,
            "followee": following_user
        })

    # User made a post request
    else:

        # Check if name value is follow
        if request.POST.get('follow'):
            follow = Follower(user=request.user, followee=User.objects.get(username=username))
            follow.save()
        
        # Check if name value if unfollow
        elif request.POST.get('unfollow'):
            # Get query of current user and profile user
            queryset = Follower.objects.filter(user=current_user, followee=username_profile)

            # Delete from Follower db
            queryset.delete()

        # Post request is Neither follow nor unfollow - User is updating their post 
        else:
            try:
                data = json.loads(request.body)
                post = Post.objects.filter(pk=data['post_id']).update(post=data['post'])
                return HttpResponse("success")
            except expression as identifier:
                return HttpResponse("error")
        return HttpResponseRedirect(f"{username}")

@login_required
@csrf_exempt
def following(request):
    '''See all posts made by users that the current user follows'''
    if request.method == "GET":
        # Get id's of users the current user is following
        query_result = Follower.objects.filter(user=request.user).values_list('followee', flat=True)

        following = [] 
        for query in query_result:
            following.append(query)

        # print(following)    
        posts_list = Post.objects.filter(user__in=following).order_by("-timestamp")
        paginator = Paginator(posts_list, 10)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        
        try:
            # Page is not the first or last
            posts = paginator.page(page_obj)
        except PageNotAnInteger:
            # First page
            posts = paginator.page(1)
        except EmptyPage:
            # Last Page
            posts = paginator.page(paginator.num_pages)

        likes = Like.objects.values('post', 'user').annotate(Count('id')).order_by('post')
        print(likes)

        return render(request, "network/follow.html", {
            "page": page_obj,
            "posts": posts,
            "likes": likes
        })
    else:
        try:
            print("in put")
            data = json.loads(request.body)
            post_instance = Post.objects.get(pk=data['post_id'])
            print(post_instance)
            user_instance = User.objects.get(pk=data['user_id'])
            print(user_instance)
            like = Like.objects.filter(post=data['post_id'], user=data['user_id']).filter(user=True) 
           
            if data['action'] == 'like':
                if not like:
                    print("new like")
                    like = Like(post=post_instance, user=user_instance)
                    like.save()
                print('outside the conditional')
            else:
                like.delete()
            return HttpResponse("success")
        except expression as identifier:
            return HttpResponse("error")
        