from django.shortcuts import render,  get_object_or_404
from .models import Schedule, Movies, Hall
from django.contrib.auth.decorators import login_required


def movies(request):
    films = Movies.objects.all()
    return render(request, 'main/movies.html', {'films': films})


def buy(request, schedule_id):
    if request.method == 'POST':
        return render(request, 'main/buy_final.html')
    else:
        scheduled = Schedule.objects.filter(pk=schedule_id)
        return render(request, 'main/buy.html', {'scheduled': scheduled})


def now_showing(request):
    scheduled = Schedule.objects.all()
    return render(request, 'main/now_showing.html', {'scheduled': scheduled})


"""
def add_movie(request):
    films = Movies.objects.all().filter()
    hall = Hall.objects.all().filter()
    time = TimeSlot.objects.all().filter()
    return render(request, 'main/add_movie.html', {'films': films, 'halls': hall, 'time': time})
"""