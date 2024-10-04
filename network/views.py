import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from .models import User, Post, Like


def index(request):
    posts = Post.objects.all()
    return render(request, "network/index.html", {
        "posts": posts
    })


def add(request):
    if request.method == "POST":
        current_user = request.user
        post_content = request.POST.get('new-content')
        if len(post_content) > 1:
            Post.objects.create(
                posted_by=current_user, content=post_content)
            return HttpResponseRedirect(reverse("index"))
        else:
            pass
    else:
        return render(request, "network/add.html")


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


# API routes

def post(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(user=request.user, pk=post_id)
    except post.DoesNotExist:
        return JsonResponse({"error": "post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update whether post is read or should be archived
    elif request.method == "PUT":
        data = json.loads(request.body)
        print(data)
        print(data["likes"])
        print(data.get("likes"))
        # data.get('likes') + 1 =

        # if data.get("read") is not None:
        #     email.read = data["read"]
        # if data.get("archived") is not None:
        #     email.archived = data["archived"]
        # email.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
