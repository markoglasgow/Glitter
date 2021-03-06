from django.shortcuts import render
from glitter_cms.models import Post, Comment
from django.http import HttpResponse

# TODO:
# User profile page

SEARCH_SETTINGS_NAMES = ["search_body", "search_title", "search_comments", "search_tags", "search_users"]


def enable_all_search_settings(request):

    for setting in SEARCH_SETTINGS_NAMES:
        request.session[setting] = '1'

    return


# Create your views here.
def search_page(request):
    context_dict = {
        'initial_load': True
    }

    search_settings = get_search_settings(request)
    for k in search_settings.keys():
        context_dict[k] = '1'

    return render(request, 'glitter_cms/search/search.html', context=context_dict)


def get_search_settings(request):
    search_settings = {}

    if 'search_body' in request.session and request.session['search_body'] == '1':
        search_settings['search_body'] = True

    if 'search_title' in request.session and request.session['search_title'] == '1':
        search_settings['search_title'] = True

    if 'search_comments' in request.session and request.session['search_comments'] == '1':
        search_settings['search_comments'] = True

    if 'search_tags' in request.session and request.session['search_tags'] == '1':
        search_settings['search_tags'] = True

    if 'search_users' in request.session and request.session['search_users'] == '1':
        search_settings['search_users'] = True

    return search_settings


def change_search_settings(request):
    search_body = request.GET.get('search_body', '')
    search_title = request.GET.get('search_title', '')
    search_comments = request.GET.get('search_comments', '')
    search_tags = request.GET.get('search_tags', '')
    search_users = request.GET.get('search_users', '')

    if len(search_body) > 0:
        request.session['search_body'] = '1'
    elif request.GET.get('ic-trigger-name', '') == 'search_body':
        request.session['search_body'] = '0'

    if len(search_title) > 0:
        request.session['search_title'] = '1'
    elif request.GET.get('ic-trigger-name', '') == 'search_title':
        request.session['search_title'] = '0'

    if len(search_comments) > 0:
        request.session['search_comments'] = '1'
    elif request.GET.get('ic-trigger-name', '') == 'search_comments':
        request.session['search_comments'] = '0'

    if len(search_tags) > 0:
        request.session['search_tags'] = '1'
    elif request.GET.get('ic-trigger-name', '') == 'search_tags':
        request.session['search_tags'] = '0'

    if len(search_users) > 0:
        request.session['search_users'] = '1'
    elif request.GET.get('ic-trigger-name', '') == 'search_users':
        request.session['search_users'] = '0'

    return HttpResponse("")


def results_page(request):
    query = request.GET.get('q', '')
    category_name = request.GET.get('cat', '')
    user_id = request.GET.get('u', '')

    post_results = []
    comment_results = []

    search_settings = get_search_settings(request)

    if len(category_name) > 0:
        result = Post.objects.filter(category__name__icontains=category_name)
        if len(result) > 0:
            post_results.append(result)

    elif len(user_id) > 0:
        result = Post.objects.filter(user__exact=int(user_id))
        if len(result) > 0:
            post_results.append(result)
        result = Comment.objects.filter(user__exact=int(user_id))
        if len(result) > 0:
            comment_results.append(result)

    elif len(query) > 0:
        if 'search_body' in search_settings:
            result = Post.objects.filter(body__icontains=query)
            if len(result) > 0:
                post_results.append(result)
        if 'search_tags' in search_settings:
            result = Post.objects.filter(tags__icontains=query)
            if len(result) > 0:
                post_results.append(result)
        if 'search_title' in search_settings:
            result = Post.objects.filter(title__icontains=query)
            if len(result) > 0:
                post_results.append(result)
        if 'search_users' in search_settings:
            result = Post.objects.filter(user__username__icontains=query)
            if len(result) > 0:
                post_results.append(result)

        if 'search_comments' in search_settings:
            result = Comment.objects.filter(body__icontains=query)
            if len(result) > 0:
                comment_results.append(result)
        if 'search_comments' in search_settings and 'search_users' in search_settings:
            result = Comment.objects.filter(user__username__icontains=query)
            if len(result) > 0:
                comment_results.append(result)
        else:
            result = Post.objects.filter(title__icontains=query)
            if len(result) > 0:
                post_results.append(result)

    context_dict = {
        'post_results': post_results,
        'comment_results': comment_results,
        'search_query': query
    }

    for k in search_settings.keys():
        context_dict[k] = '1'

    return render(request, 'glitter_cms/search/search.html', context=context_dict)
