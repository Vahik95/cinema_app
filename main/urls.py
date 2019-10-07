from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.movies, name='movies'),
    url(r'^(?P<movie_id>[0-9]+)/', views.movie_details, name='movie_details'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
