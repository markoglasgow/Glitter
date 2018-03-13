from __future__ import unicode_literals

from django.db import models

CATEGORY_COLOURS = {
    'Announcements': 'lightskyblue',
    'Coursework': 'lightsalmon',
    'Misc': 'lightgreen'
}

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255)
    password_hash = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    student_id = models.CharField(max_length=50)
    recovery_token = models.CharField(max_length=255)


class Category(models.Model):
    name = models.CharField(max_length=255)

    def calculateColour(self):
        return CATEGORY_COLOURS[self.name]

    colour = property(calculateColour)

class Post(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    timestamp = models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    body = models.TextField()
    tags = models.CharField(max_length=255)
    likes_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)



class Comment(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    timestamp = models.IntegerField(default=0)
    body = models.TextField()
    likes_count = models.IntegerField(default=0)


# TODO: This model will probably require reworking.
class Likes(models.Model):
    user = models.ForeignKey(User)
    liked_post = models.ForeignKey(Post, null=True)
    liked_comment = models.ForeignKey(Comment, null=True)
