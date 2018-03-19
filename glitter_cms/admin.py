from django.contrib import admin
from glitter_cms.models import Category, Post, Comment, Likes, Profile

# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Likes)
admin.site.register(Profile)
