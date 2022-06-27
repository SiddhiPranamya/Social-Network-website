from sqlite3 import Timestamp
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import User, Post, Follow


def index(request):
    message=""
    if request.method == "POST":
        object = Post()
        object.user = request.user
        if(request.POST.get('post')!= ""):
            object.post = request.POST.get('post')
        else:
            message= "Cannot create post with empty text"
        object.timestamp = Timestamp.now()
        object.save()
    posts = Post.objects.all().order_by('-timestamp')#arranging from most recent post first 
        
    paginator = Paginator(posts, 10) # Show 10 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",{
        "posts": posts,
        "message": message,
        "page_obj": page_obj
    })

@login_required
def profile(request,owner):
    owner = User.objects.get(id=owner)
    button = "Follow" if Follow.objects.filter(follower=request.user, following=owner).count() == 0 else "Unfollow"

    if request.method == "POST":
        if request.POST["button"] == "Follow":
            button = "Unfollow"
            Follow.objects.create(follower=request.user, following=owner)
        else:
            button = "Follow"
            Follow.objects.get(follower=request.user, following=owner).delete()
    posts = Post.objects.filter(user=owner.id).order_by('-timestamp'),#arranging from most recent post first 
    
    paginator = Paginator(posts, 10) # Show 10 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html",{
        "posts": posts,   
        "owner": owner, 
        "followers": Follow.objects.filter(following=owner).count(), 
        "following": Follow.objects.filter(follower=owner).count(),  
        "button": button,
        "page_obj": page_obj
    })
    
@login_required
def following(request):
    following = Follow.objects.filter(follower=request.user).values('following_id')
    posts = Post.objects.filter(user__in=following).order_by('-timestamp') 
    return render(request, "network/following.html",{
        "posts": posts,
    })

@csrf_exempt
@login_required
def edit(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == "POST":
        data = json.loads(request.body)
        if data.get("post") is not None:
            post.post = data["post"]
        post.save()
        return HttpResponse(status=204)


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
