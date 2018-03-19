from django.conf.urls import url

from glitter_cms import views
from glitter_cms import views_login
from glitter_cms import views_posts
from glitter_cms import views_search
from glitter_cms import views_profiles

# noinspection PyInterpreter
urlpatterns = [
    url(r'^$', views.index, name='index'),

    # Comments
    url(r'^view_post/(?P<post_id>[\w\-]+)/add_comment/$', views_posts.add_comment, name='add_comment'),
    url(r'^view_post/(?P<post_id>[\w\-]+)/(?P<comment_id>[\w\-]+)/delete_comment/$', views_posts.delete_comment, name='delete_comment'),
    url(r'^view_post/(?P<post_id>[\w\-]+)/(?P<comment_id>[\w\-]+)/update_comment/$', views_posts.update_comment, name='update_comment'),
    url(r'^view_post/(?P<post_id>[\w\-]+)/(?P<comment_id>[\w\-]+)/like_comment/$', views_posts.like_comment, name='like_comment'),

    # Posts
    url(r'^view_post/(?P<post_id>[\w\-]+)/$', views_posts.view_post, name='view_post'),
    url(r'^create_post/$', views_posts.create_post, name='create_post'),
    url(r'^view_post/(?P<post_id>[\w\-]+)/update_post/$', views_posts.update_post, name='update_post'),
    url(r'^view_post/(?P<post_id>[\w\-]+)/delete_post/$', views_posts.delete_post, name='delete_post'),
    url(r'^view_post/(?P<post_id>[\w\-]+)/like_post/$', views_posts.like_post, name='like_post'),



    # URL patterns for login go here...
    url(r'^login/$', views_login.user_login, name='login'),

    # URL patterns for search functionality goes here...
    url(r'^search/change_search_settings$', views_search.change_search_settings, name='change_search_settings'),
    url(r'^search/q$', views_search.results_page, name='results_page'),
    url(r'^search/$', views_search.search_page, name='search_page'),

    # URL patterns for viewing user profiles go here
    url(r'^public_profile/(?P<user_id>[\w\-]+)/$', views_profiles.public_user_profile, name='public_user_profile'),
    url(r'^private_profile/$', views_profiles.private_user_profile, name='private_user_profile'),

    url(r'^login/$', views_login.user_login, name='login'),
    url(r'^register/$',views_login.register,name='register'),
    url(r'^logout/$', views_login.user_logout, name='logout'),
    url(r'^password/$', views_login.change_password, name='password_change'),

]


