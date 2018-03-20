from django.shortcuts import render
from glitter_cms.models import Post
from datetime import datetime

POST_VIEW_COUNT = 5

# Create your views here.
def index(request):
    posts = Post.objects.order_by('-timestamp')[:POST_VIEW_COUNT]
    context_dict = {'posts': posts}

    return render(request, 'glitter_cms/index.html', context = context_dict)
    

