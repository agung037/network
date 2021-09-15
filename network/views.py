import os
import json
import secrets
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage

from .models import User, Post, Follow, Comment, Like


def comment(request):
    if request.method == "POST":
        page_num = request.POST.get("page-num")
        if not page_num:
            page_num = 1
        comment = request.POST.get("comment")
        post_id = request.POST.get("post-id")
        post = Post.objects.get(id=post_id)

        c = Comment(post=post, user=request.user, comment=comment).save()

    return redirect("/home/all")


def edit_profile(request, username):
    if request.method == "POST":
        firstName = request.POST["firstName"]
        lastName = request.POST["lastName"]
        job = request.POST["job"]
        about = request.POST["about"]
        education = request.POST["education"]
        avatar = request.POST["avatar"]

        obj = User.objects.get(username=username)
        obj.firstName = firstName
        obj.lastName = lastName
        obj.job = job
        obj.about = about
        obj.education = education
        obj.avatar = avatar
        obj.save()

    return redirect('profile', username=username)


def get_with_ajax(request):
    return JsonResponse({'foo': 'bar'})


def edit_post(request):
    if request.method == "POST":
        edited_post = request.POST["edited-post"]
        print(edited_post)

    return redirect("/")


def following_post(request):
    pass


def index(request, route):
    my_post = Post.objects.all().order_by('-pub_date')

    if route == "all":
        # get all post
        my_post = Post.objects.all().order_by('-pub_date')
    
    if route == "follow":
        # get post by followed user
        current_user_follow = Follow.objects.get(person=request.user)
        my_post = Post.objects.filter(user__in=current_user_follow.following.all()).order_by('-pub_date')

    total_post = my_post.count()
    post_per_page = 10

    # paginator in action
    pagi = Paginator(my_post, post_per_page)
    page_num = request.GET.get('page', 1)
    total_pages = pagi.num_pages
    pages_number_list = [n+1 for n in range(total_pages)]

    try:
        my_post = pagi.page(page_num)
    except EmptyPage:
        my_post = pagi.page(1)
    
    # update like data
    like_data_on_page = Like.objects.filter(post__in=my_post)
    
    for post in my_post:
        # cari like untuk tiap individual post
        jumlah_like = Like.objects.filter(post=post).count()

        # update ke masing masing post model
        obj = Post.objects.get(id=post.id)
        obj.like = jumlah_like
        obj.save() 

    # comments
    comments = Comment.objects.filter(post__in=my_post)

    # liked post
    all_liked_post = []
    try:
        liked_post = Like.objects.filter(user=request.user)
    except:
        liked_post = []
    
    for like in liked_post:
        all_liked_post.append(like.post.id)


    # get latest data
    try:
        my_post = pagi.page(page_num)
    except EmptyPage:
        my_post = pagi.page(1)


    return render(request, "network/index.html", {
        "post_content": my_post,
        "pages_number_list": pages_number_list,
        "comments": comments,
        "liked_post": all_liked_post,
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
            return HttpResponseRedirect("home/all")
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("home/all/")


def post(request):
    if request.method == "POST":
        user = request.user
        post = request.POST["post"]
        create_post = Post(
            post=post, user=user, url_token=secrets.token_urlsafe(
                8)).save()

    return HttpResponseRedirect("home/all")


def edit_post_with_ajax(request):
    data = json.loads(request.body)
    u = Post.objects.get(id=data["id"])
    if u.user == request.user:
        u.post = data["text"]
        u.save()
        return JsonResponse({'status': 'edit data berhasil'})
    return JsonResponse({'status': 'edit data gagal'})


def follow_with_ajax(request):
    data = json.loads(request.body)
    if data["type"] == "follow":
        t = User.objects.get(username=data["person"])
        f = Follow.objects.get(person = request.user)
        f.following.add(t)
    else:
        t = User.objects.get(username=data["person"])
        f = Follow.objects.get(person = request.user)
        f.following.remove(t)
    return JsonResponse({'status': 'follow berhasil'})

def like(request):
    data = json.loads(request.body)
    post_id = int(data["id"])
    postingan = Post.objects.get(id=post_id)

    # cek apakah sudah pernah like
    like_data = Like.objects.filter(user=request.user, post=postingan)
    
    # jika belum pernah like
    if not like_data:
        like = Like(user=request.user, post=postingan)
        like.save()
        # hitung jumlah like
        total_like = Like.objects.filter(post=postingan).count()
        return JsonResponse({
            'like': 'tercatat',
            'totalLike': total_like
            })
   
    like_data.delete()  # jika sudah ada like maka hapus

    # hitung jumlah like
    total_like = Like.objects.filter(post=postingan).count()
    return JsonResponse({
        'like': 'terhapus',
        'totalLike': total_like
        })


def profile(request, username):
    try:
        user = User.objects.get(username=username)
      
        # followers
        followers = user.set_followings.all()
        followers_count = followers.count()
        followers_name = []
        followers_object = []
        for f in followers:
            followers_name.append(str(f))

        for f in followers_name:
            x = User.objects.get(username=f)
            followers_object.append(x)

        # followings
        try:
            followings_list = Follow.objects.get(person=user)
        except:
            followings_list = []

        # current user following data
        try :
            current_user_follow = Follow.objects.get(person=request.user)
        except:
            current_user_follow = []

        # dapatkan seluruh post dari user
        my_post = Post.objects.filter(user=user)
        
        total_post = my_post.count()
        post_per_page = 10

        # paginator in action
        pagi = Paginator(my_post, post_per_page)
        page_num = request.GET.get('page', 1)
        total_pages = pagi.num_pages
        pages_number_list = [n+1 for n in range(total_pages)]

        try:
            my_post = pagi.page(page_num)
        except EmptyPage:
            my_post = pagi.page(1)
        
        # update like data
        like_data_on_page = Like.objects.filter(post__in=my_post)
        
        for post in my_post:
            # cari like untuk tiap individual post
            jumlah_like = Like.objects.filter(post=post).count()

            # update ke masing masing post model
            obj = Post.objects.get(id=post.id)
            obj.like = jumlah_like
            obj.save() 

        # comments
        comments = Comment.objects.filter(post__in=my_post)

        # liked post
        all_liked_post = []
        try:
            liked_post = Like.objects.filter(user=request.user)
        except:
            liked_post = []
        
        for like in liked_post:
            all_liked_post.append(like.post.id)


        # get latest data
        try:
            my_post = pagi.page(page_num)
        except EmptyPage:
            my_post = pagi.page(1)
        

    except User.DoesNotExist:
        return render(request, "network/error.html")

    return render(request, "network/profile.html", {
       "user": user,
       "followers": followers_object,
       "followers_count": followers_count,
       "followings_list": followings_list,
       "current_user_follow": current_user_follow,
       "post_content": my_post,
       "comments": comments,
       "liked_post": all_liked_post,

    })


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

            # create follow
            f = Follow(person=user)
            f.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect("home/all")
    else:
        return render(request, "network/register.html")
