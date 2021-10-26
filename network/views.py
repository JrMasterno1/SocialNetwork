from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime as dt
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.core.paginator import Paginator

from .models import User, Post, User_Post_like, Comment


def index(request):
    if request.method == "POST":
        content = request.POST["content"]
        name = request.user
        d = dt.datetime.now()
        Post.objects.create(user=name, content=content, date=d, like=0)
    like = []
    if request.user.is_authenticated:
        u = User.objects.get(id=request.user.id)
        try:
            liked = User_Post_like.objects.filter(user=u)
            for instance in liked:
                like.append(instance.post)
        except User_Post_like.DoesNotExist:
            like = []
    posts = Post.objects.order_by('-date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    comments = Comment.objects.all()
    return render(request, "network/index.html", {
        "liked": like,
        'page_obj' : page_obj,
        "comments": comments
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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def like(request, id):
    if request.method == "PUT":
        data = json.loads(request.body)
        p = Post.objects.get(id=id)
        u = User.objects.get(id=request.user.id)
        done = False
        try:
            User_Post_like.objects.get(post=p, user=u)
        except User_Post_like.DoesNotExist:
            p.like += 1
            p.save()
            User_Post_like.objects.create(post=p, user=u)
            done = True
            return index(request)
        if not done:
            p.like -= 1
            p.save()
            User_Post_like.objects.filter(post=p, user=u).delete()
            return index(request)
    return index(request)
def user(request, id):
    return render(request, "network/user.html", {
        "user": User.objects.get(id=id)
    })
@csrf_exempt
@login_required
def comment(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get('content')
        p = Post.objects.get(id=id)
        u = User.objects.get(id=request.user.id)
        Comment.objects.create(user=u, post=p, content=content)
        return HttpResponse(status=204)
    return index(request)

