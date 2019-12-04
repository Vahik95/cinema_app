from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path


urlpatterns = [
    url(r'^$', views.movies, name='movies'),
    url(r'^cinemas/', views.cinemas, name='cinemas'),

    url(r'^(?P<movie_id>[0-9]+)/', views.movie_details, name='movie_details'),
    url(r'^buy/(?P<schedule_id>[0-9]+)/', views.buy, name='buy'),
    url(r'^check/(?P<schedule_id>[0-9]+)/', views.check, name='check'),
    url(r'^buy_final', views.buy, name='buy'),
    url(r'^checkout/(?P<schedule_id>[0-9]+)/', views.checkout, name='checkout'),
    url(r'^now_showing', views.now_showing, name='now_showing'),
    url(r'^cinema_schedule/(?P<cinema_id>[0-9]+)/', views.cinema_schedule, name='cinema_schedule'),
    url(r'^cinema_about(?P<cinema_id>[0-9]+)/', views.cinema_about, name='cinema_about'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
