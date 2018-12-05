from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.movies, name='movies'),
    url(r'^buy/(?P<schedule_id>[0-9]+)/$', views.buy, name='buy'),
    url(r'^check/(?P<schedule_id>[0-9]+)/$', views.check, name='check'),
    url(r'^buy_final', views.buy, name='buy'),
    url(r'^now_showing', views.now_showing, name='now_showing'),
    # url(r'^add_movie', views.add_movie, name='add_movie'),
]