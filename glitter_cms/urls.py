from django.conf.urls import url

from glitter_cms import views
from glitter_cms import views_login
from glitter_cms import views_posts
from glitter_cms import views_search

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    url(r'^$', views.index, name='index'),


    # URL patterns for create/view/edit/delete posts goes here...
    url(r'^view_post/$', views_posts.view_page, name='view_post'),
    url(r'^login/$', views_login.user_login, name='login'),
    # URL patterns for search functionality goes here...
    url(r'^search/$', views_search.search_page, name='search_page'),
    url(r'^register/$',views_login.register,name='register'), # New pattern!
    url(r'^logout/$', views_login.user_logout, name='logout'),
    url(r'^password/$', views_login.change_password, name='password_change'),

]


