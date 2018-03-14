from django.shortcuts import render
from glitter_cms.models import Post

POST_VIEW_COUNT = 5

# Create your views here.
def index(request):
    posts = Post.objects.order_by('-timestamp')[:POST_VIEW_COUNT]
    context_dict = {'posts': posts}

    response = render(request, 'glitter_cms/index.html', context = context_dict)
    return response
