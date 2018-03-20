from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from glitter_cms.models import Post, Comment, User, Category
from glitter_cms.forms import CommentForm, PostForm
import calendar
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
def view_post(request, post_id):
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

@login_required
def create_post(request):
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        user = None

    context_dict = {}
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            if user:
                post = form.save(commit=False)
                post.user = user
                post.category = form.cleaned_data['category']
                post.timestamp = calendar.timegm(datetime.utcnow().utctimetuple())
                post.title = form.cleaned_data['title']
                post.body = form.cleaned_data['body']
                post.tags = form.cleaned_data['tags']
                post.likes_count = 0
                post.reply_count = 0
                post.view_count = 0
                post.save()

                return redirect('index')

    context_dict['form'] = form
    return render(request, 'glitter_cms/post/create_post.html', context_dict)

@login_required
def update_post(request, post_id):
    try:
        user = User.objects.get(id=request.user.id)
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist or User.DoesNotExist:
        return redirect('index')

    context_dict = {}
    form = PostForm(initial={'title': post.title, 'body': post.body, 'tags':post.tags, 'category':post.category})

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            if user:
                post.category = form.cleaned_data['category']
                post.timestamp = calendar.timegm(datetime.utcnow().utctimetuple())
                post.title = form.cleaned_data['title']
                post.body = form.cleaned_data['body']
                post.tags = form.cleaned_data['tags']

                post.save()

                return redirect('view_post', post_id=post_id)

    context_dict['form'] = form
    context_dict['post'] = post_id
    return render(request, 'glitter_cms/post/update_post.html', context_dict)


@login_required
def like_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return redirect('index')

    post.likes_count = post.likes_count + 1
    post.save()

    return redirect('view_post', post_id=post_id)

@login_required
def delete_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return redirect('index')

    if post.reply_count > 0:
        comments = Comment.objects.filter(post=post).delete()

    post.delete()
    return redirect('index')

@login_required
def add_comment(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        user = User.objects.get(id=request.user.id)
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

                return redirect('view_post', post_id=post_id)

        return redirect('view_post', post_id=post_id)

@login_required
def update_comment(request, post_id, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        post = Post.objects.get(id=post_id)
    except Comment.DoesNotExist:
        return index(request)

    context_dict = {}
    form = CommentForm(initial={'body': comment.body})
    post.reply_count = post.reply_count - 1
    post.save()

    comment.delete()
    context_dict['form'] = form
    context_dict['post'] = post_id
    return render(request, 'glitter_cms/post/update_comment.html', context_dict)

@login_required
def like_comment(request, post_id, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return index(request)

    comment.likes_count = comment.likes_count + 1
    comment.save()

    return redirect('view_post', post_id=post_id)

@login_required
def delete_comment(request, post_id, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return index(request)

    post = Post.objects.get(id=post_id)
    post.reply_count = post.reply_count - 1
    if post.reply_count < 0:
        post.reply_count = 0
    post.save()

    comment.delete()

    return redirect('view_post', post_id=post_id)
