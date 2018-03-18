from django.shortcuts import render, redirect
from glitter_cms.models import Post, Comment, User, Category
from glitter_cms.forms import CommentForm, PostForm
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

    #todo
    # Retrieve user from session as opposed to hard coded ID.

def create_post(request):
    try:
        user = User.objects.get(id=1)
    except User.DoesNotExist:
        user = None

    context_dict = {}
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            cat = Category.objects.get(name=form.cleaned_data['category'])
            if user and category:
                post = form.save(commit=False)
                post.user = user
                post.category = cat
                post.timestamp = calendar.timegm(datetime.utcnow().utctimetuple())
                post.title = form.cleaned_data['title']
                post.body = form.cleaned_data['body']
                post.tags = form.cleaned_data['tags']
                post.likes_count = 0
                post.reply_count = 0
                post.view_count = 0
                post.save()

                print('Post Saved')
                return index(request)

    context_dict['form'] = form
    return render(request, 'glitter_cms/post/create_post.html', context_dict)



def add_comment(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        user = User.objects.get(id=1)
    except Post.DoesNotExist:
        post = None
        user = None


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

