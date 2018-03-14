from django.shortcuts import render
from glitter_cms.models import Post, Comment
from django.http import HttpResponse


def public_user_profile(request):
    return HttpResponse("Hello world")