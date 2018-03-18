from django.shortcuts import render
from glitter_cms.models import Post
from datetime import datetime

POST_VIEW_COUNT = 5

# Create your views here.
def index(request):
    posts = Post.objects.order_by('-timestamp')[:POST_VIEW_COUNT]
    context_dict = {'posts': posts}

    response = render(request, 'glitter_cms/index.html', context = context_dict)
    visitor_cookie_handler(request)
    return response

# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val
# Updated the function definition
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val
# Updated the function definition
def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                                'last_visit',
                                                str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
# If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
#update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
# set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
# Update/set the visits cookie
    request.session['visits'] = visits
