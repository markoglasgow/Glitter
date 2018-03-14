from django.shortcuts import render
from glitter_cms.models import Post, Comment, User
from glitter_cms.forms import CommentForm
import calendar
from datetime import datetime

# Create your views here.
def view_page(request, post_id):
    context_dict = {}
    form = CommentForm()

    try:
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post)

        context_dict['post'] = post
        context_dict['comments'] = comments
        context_dict['form'] = form

    except Post.DoesNotExist:
        context_dict['post'] = None
        context_dict['comments'] = None

    return render(request, 'glitter_cms/post/view_post.html', context_dict)


def add_comment(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        user = User.objects.get(id=1)
    except Post.DoesNotExist:
        post = None
        user = None

    #todo
    # Retrieve user from session as opposed to hard coded ID.

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if post and user:
                comment = form.save(commit=False)
                comment.body = form.cleaned_data['body']
                comment.post = post
                comment.likes_count = 0
                comment.timestamp = calendar.timegm(datetime.utcnow().utctimetuple())
                comment.user = user
                comment.save()

                # Increase comment count for parent post.
                post.reply_count = post.reply_count + 1
                post.save()

                return view_page(request, post_id)

    return view_page(request, post_id)
