from django.contrib import admin
from glitter_cms.models import User, Category, Post, Comment, Likes, UserProfile

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Likes)
admin.site.register(UserProfile)
