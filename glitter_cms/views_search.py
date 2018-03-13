from django.shortcuts import render
from glitter_cms.models import Post, Comment

# TODO:
# Save search settings upon modification

# Sorting?
# Pagination?

# User profile page


# Create your views here.
def search_page(request):
    return render(request, 'glitter_cms/search/search.html')


def results_page(request):
    query = request.GET.get('q', '')
    category_name = request.GET.get('cat', '')
    user_id = request.GET.get('u', '')

    post_results = []
    comment_results = []

    if len(category_name) > 0:
        result = Post.objects.filter(category__name__icontains=category_name)
        if len(result) > 0:
            post_results.append(result)

    elif len(user_id) > 0:
        result = Post.objects.filter(user__exact=int(user_id))
        if len(result) > 0:
            post_results.append(result)

    elif len(query) > 0:
        result = Post.objects.filter(body__icontains=query)
        if len(result) > 0:
            post_results.append(result)
        result = Post.objects.filter(tags__icontains=query)
        if len(result) > 0:
            post_results.append(result)
        result = Post.objects.filter(title__icontains=query)
        if len(result) > 0:
            post_results.append(result)
        result = Post.objects.filter(user__name__icontains=query)
        if len(result) > 0:
            post_results.append(result)

        result = Comment.objects.filter(body__icontains=query)
        if len(result) > 0:
            comment_results.append(result)
        result = Comment.objects.filter(user__name__icontains=query)
        if len(result) > 0:
            comment_results.append(result)

    context_dict = {
        'post_results': post_results,
        'comment_results': comment_results,
        'search_query': query
    }

    return render(request, 'glitter_cms/search/search.html', context=context_dict)
