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

from .models import User, Post, Like


def index(request):
    posts = Post.objects.all().order_by('-id')
    return render(request, "network/index.html", {
        "posts": posts
    })


# add new post
def add(request):
    if request.method == "POST":
        current_user = request.user
        post_content = request.POST.get('new-content')
        print("post content =")
        print(post_content)
        if post_content == "":
            return JsonResponse({"error": "At least one character required."
                                 }, status=400)
        Post.objects.create(
            posted_by=current_user, content=post_content)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/add.html")


# API routes

def post(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(posted_by=request.user, pk=post_id)
    except post.DoesNotExist:
        return JsonResponse({"error": "post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update post
    elif request.method == "PUT":
        data = json.loads(request.body)
        print(data)
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@csrf_exempt
def editlike(request):
    data = json.loads(request.body)
    print(data)
    print(Like.objects.filter(
        liked_by=request.user, liked_post=data.get("liked_post")).exists())
    like_exists = Like.objects.filter(
        liked_by=request.user, liked_post=data.get("liked_post")).exists()
    if like_exists == True:
        existing_like = Like.objects.filter(
            liked_by=request.user, liked_post=data.get("liked_post"))
        existing_like.delete()
        print("went to try")
        return HttpResponseRedirect(reverse("index"))
    else:
        print("went to else")
        post_id = data.get("liked_post")
        liked_post = Post.objects.get(pk=post_id)
        print(liked_post)
        print(liked_post.id)
        new_like = Like.objects.create(
            liked_by=request.user, liked_post=liked_post)
        new_like.save()
        return JsonResponse(new_like.serialize())


def likeinfo(request, like_id):
    # Query for requested like
    try:
        like = Like.objects.get(liked_by=request.user, pk=like_id)
    except Like.DoesNotExist:
        return JsonResponse({"error": "like not found."}, status=404)

    # Return like content
    if request.method == "GET":
        return JsonResponse(like.serialize())

    # create new like
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
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
