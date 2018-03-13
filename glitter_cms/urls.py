from django.conf.urls import url

from glitter_cms import views
from glitter_cms import views_login
from glitter_cms import views_posts
from glitter_cms import views_search


urlpatterns = [
    url(r'^$', views.index, name='index'),

    # URL patterns for login go here...
    url(r'^login/$', views_login.login_page, name='login'),

    # URL patterns for create/view/edit/delete posts goes here...
    url(r'^view_post/$', views_posts.view_page, name='view_post'),

    # URL patterns for search functionality goes here...
    url(r'^search/q$', views_search.results_page, name='results_page'),
    url(r'^search/$', views_search.search_page, name='search_page'),
]
