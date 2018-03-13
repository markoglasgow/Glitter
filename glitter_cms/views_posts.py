from django.shortcuts import render
from glitter_cms.models import Post, Comment

# Create your views here.
def view_page(request, post_id):
    context_dict = {}

    try:
        post = Post.objects.get(pk=post_id)
        comments = Comment.objects.filter(post=post)

        context_dict['post'] = post
        context_dict['comments'] = comments

    except Post.DoesNotExist:
        context_dict['post'] = None
        context_dict['comments'] = None

    return render(request, 'glitter_cms/post/view_post.html', context_dict)
