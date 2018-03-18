from django.conf.urls import url

from glitter_cms import views
from glitter_cms import views_login
from glitter_cms import views_posts
from glitter_cms import views_search
from glitter_cms import views_profiles

# noinspection PyInterpreter
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^view_post/(?P<post_id>[\w\-]+)/add_comment/$', views_posts.add_comment, name='add_comment'),
    url(r'^create_post/$', views_posts.create_post, name='create_post'),

    # URL patterns for login go here...
    url(r'^login/$', views_login.login_page, name='login'),

    # URL patterns for create/view/edit/delete posts goes here...
    url(r'^view_post/(?P<post_id>[\w\-]+)/$', views_posts.view_page, name='view_post'),

    # URL patterns for search functionality goes here...
    url(r'^search/change_search_settings$', views_search.change_search_settings, name='change_search_settings'),
    url(r'^search/q$', views_search.results_page, name='results_page'),
    url(r'^search/$', views_search.search_page, name='search_page'),

    # URL patterns for viewing user profiles go here
    url(r'^public_profile/$', views_profiles.public_user_profile, name='public_user_profile'),
]
