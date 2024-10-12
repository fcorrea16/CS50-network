import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import Count

from .models import User, Post, Like, Follower


def index(request):
    posts = Post.objects.all().order_by('-id')
    posts_liked = []
    if request.user.is_authenticated:
        posts_liked_by_user = Like.objects.filter(liked_by=request.user)
        for post in posts_liked_by_user:
            test = post.liked_post.id
            posts_liked.append(test)
    return render(request, "network/index.html", {
        "posts": posts, "posts_liked": posts_liked})


def following(request):
    ruser = request.user.id
    all_following = Follower.objects.filter(user_id=ruser).all()
    all_posts = Post.objects.all().order_by('-id')
    following_post_ids = []
    for post in all_posts:
        for following in all_following:
            if following.follower == post.posted_by:
                following_post_ids.append(post.id)
            else:
                pass
    following_posts = []
    for post in following_post_ids:
        following_posts.append(Post.objects.filter(pk=post))
    print(following_posts)

    posts_liked = []
    posts_liked_by_user = Like.objects.filter(liked_by=request.user)
    for post in posts_liked_by_user:
        test = post.liked_post.id
        posts_liked.append(test)
    return render(request, "network/following.html",
                  {"all_following": all_following,
                   "following_posts": following_posts, "all_posts": all_posts, "posts_liked": posts_liked})


def profile(request, username):
    username = get_object_or_404(User, username=username)
    request_user = request.user
    posts_by_user = Post.objects.filter(posted_by=username).order_by('-id')
    all_following = Follower.objects.filter(user_id=username).all()
    following_num = all_following.count()
    all_followers = Follower.objects.filter(follower=username).all()
    followers_num = all_followers.count()
    request_user_follows = False
    request_user_follows_id = 0
    posts_liked = []
    if request.user.is_authenticated:
        posts_liked_by_user = Like.objects.filter(liked_by=request.user)
        for post in posts_liked_by_user:
            test = post.liked_post.id
            posts_liked.append(test)
        if Follower.objects.filter(user_id=request.user, follower=username).exists():
            request_user_follows = Follower.objects.filter(
                user_id=request.user, follower=username).exists()
            request_user_follows_id = Follower.objects.get(
                user_id=request.user, follower=username).id
        else:
            request_user_follows = False
            request_user_follows_id = 0
    else:
        pass
    return render(request, "network/profile.html", {
        "request_user": request_user, "username": username, "posts_by_user": posts_by_user, "following_num": following_num,
        "followers_num": followers_num, "posts_liked": posts_liked, "request_user_follows": request_user_follows, "request_user_follows_id": request_user_follows_id})


# API routes

# add new post
def add(request):
    if request.method == "POST":
        current_user = request.user
        post_content = request.POST.get('new-content')
        if post_content == "":
            return JsonResponse({"error": "At least one character required."
                                 }, status=400)
        Post.objects.create(
            posted_by=current_user, content=post_content)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/index.html")


@csrf_exempt
def post(request, post_id):

    # Query for requested post
    post = get_object_or_404(Post, pk=post_id)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update post
    elif request.method == "PUT":
        data = json.loads(request.body)
        post = Post.objects.get(posted_by=request.user, pk=post_id)
        post.content = data["content"]
        post.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


# add new follower
def follow(request):
    if request.method == "POST":
        ruser = request.user
        follower = User.objects.get(username=ruser)
        follow_name = request.POST.get("profile_user")
        follow = User.objects.get(username=follow_name)
        new_follow = Follower.objects.create(
            user_id=follower, follower=follow)
        new_follow.save()
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    else:
        return render(request, "network/index.html")


@csrf_exempt
def follower(request, follower_id):

    # Query for requested post
    follower_id = get_object_or_404(Follower, pk=follower_id)
    print(follower_id)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(follower_id.serialize())

    # Update post
    elif request.method == "PUT":
        # print("hi put")
        # data = json.loads(request.body)
        return HttpResponse(status=204)

    elif request.method == "DELETE":
        data = json.loads(request.body)
        follower_id = data.get("follower_id")
        Follower.objects.get(id=follower_id).delete()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "GET or PUT or delete request required."
        }, status=400)


@csrf_exempt
def editlike(request):
    data = json.loads(request.body)
    user = request.user
    post_id = data.get("liked_post")
    like_exists = Like.objects.filter(
        liked_by=user, liked_post=post_id).exists()
    post = Post.objects.get(id=post_id)
    if like_exists == True:
        existing_like = Like.objects.get(
            liked_by=user, liked_post=post_id)
        existing_like.delete()
        post.likes.remove(user)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        new_like = Like.objects.create(
            liked_by=user, liked_post=post)
        new_like.save()
        post.likes.add(user)
        post.save()
        return JsonResponse(new_like.serialize())


def likeinfo(request, like_id):
    # Query for requested like
    try:
        like = Like.objects.get(pk=like_id)
    except Like.DoesNotExist:
        return JsonResponse({"error": "like not found."}, status=404)

    # Return like content
    if request.method == "GET":
        return JsonResponse(like.serialize())

    # anything that isnt get
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)


# LOGIN /LOGOUT/REGISTER

@csrf_protect
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


@csrf_protect
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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
