from django.conf.urls import url

from glitter_cms import views
from glitter_cms import views_login
from glitter_cms import views_posts
from glitter_cms import views_search
from glitter_cms import views_profiles

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.index, name='index'),

    # URL patterns for create/view/edit/delete posts goes here...
    url(r'^view_post/(?P<post_id>[\w\-]+)/$', views_posts.view_page, name='view_post'),
    
    # URL patterns for search functionality goes here...
    url(r'^search/change_search_settings$', views_search.change_search_settings, name='change_search_settings'),
    url(r'^search/q$', views_search.results_page, name='results_page'),
    url(r'^search/$', views_search.search_page, name='search_page'),

    # URL patterns for viewing user profiles go here
    url(r'^public_profile/$', views_profiles.public_user_profile, name='public_user_profile'),
    url(r'^private_profile/$', views_profiles.private_user_profile, name='private_user_profile'),

    url(r'^login/$', views_login.user_login, name='login'),
    url(r'^register/$',views_login.register,name='register'),
    url(r'^logout/$', views_login.user_logout, name='logout'),
    url(r'^password/$', views_login.change_password, name='password_change'),

]


