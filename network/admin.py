from django.contrib import admin
from .models import *


@admin.register(Post)
class Post(admin.ModelAdmin):
    list_display = ("user", "pub_date", "post", "like")


@admin.register(User)
class User(admin.ModelAdmin):
    pass


@admin.register(Follow)
class Follow(admin.ModelAdmin):
    pass


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ("post", "user", "comment")


@admin.register(Like)
class Like(admin.ModelAdmin):
    list_display = ("post", "user")
