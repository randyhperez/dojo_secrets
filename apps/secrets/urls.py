from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^log_reg/$', views.log_reg, name='log_reg'),
    url(r'^secrets/$', views.secrets, name='secrets'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^post/$', views.post, name='post'),
    url(r'^likes/(?P<secret_id>\d+)$', views.likes, name='likes'),
    url(r'^delete/(?P<secret_id>\d+)$', views.delete, name='delete'),
    url(r'^popular/$', views.popular, name='popular'),
]
