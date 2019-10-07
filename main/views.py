from django.shortcuts import render, get_object_or_404, redirect
from .models import Movies
from django.contrib.auth.decorators import login_required
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def movies(request):
    movies_list = Movies.objects.all().order_by('-id')
    paginator = Paginator(movies_list, 3) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        movies = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        movies = paginator.page(paginator.num_pages)

    return render(request, 'main/movies.html', {'films': movies})


def movie_details(request, movie_id):
    movie = Movies.objects.filter(pk=movie_id)
    return render(request, 'main/movie_details.html', {'movie':movie})
