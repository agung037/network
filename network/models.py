from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.CharField(max_length=250, blank=True, null=True, default="https://www.pngitem.com/pimgs/m/146-1468479_my-profile-icon-blank-profile-picture-circle-hd.png")
    firstName = models.CharField(max_length=75, blank=True, null=True, default="John")
    lastName = models.CharField(max_length=75, blank=True, null=True, default="Doe")
    job = models.CharField(max_length=75, blank=True, null=True)
    education = models.CharField(max_length=125, blank=True, null=True)
    about = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return str(self.username)


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    post = models.TextField(blank=True, null=True)
    url_token = models.CharField(
        max_length=20, blank=True, null=True)
    like = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "author : " + str(self.user) + " | post content : " + str(self.post)


class Follow(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='the_followers', blank=True, null=True)
    following = models.ManyToManyField(User, related_name='set_followings', blank=True, null=True)

    def __str__(self):
        return str(self.person)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='list_post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, blank=True, null=True)
    pub_date = models.DateTimeField(auto_now=True, blank=True, null=True) 

    def __str__(self):
        return str(self.post) + " " + str(self.comment)


class Like(models.Model):
    post = models.ForeignKey(Post, related_name="post_liked",  on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="liker", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.post)