from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


CATEGORY_COLOURS = {
    'Announcements': 'lightskyblue',
    'Coursework': 'lightsalmon',
    'Misc': 'lightgreen'
}


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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=50)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

