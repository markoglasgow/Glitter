from django.conf.urls import url
from glitter_cms import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
