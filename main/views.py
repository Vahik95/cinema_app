from django.shortcuts import render, get_object_or_404
from .models import Schedule, Movies, Hall, Seat
from django.contrib.auth.decorators import login_required


def movies(request):
    films = Movies.objects.all()
    return render(request, 'main/movies.html', {'films': films})


def buy(request, schedule_id):
    if request.method == 'POST':
        return render(request, 'main/buy_final.html', {'schedule_id': schedule_id})
    else:
        scheduled = Schedule.objects.filter(pk=schedule_id)
        return render(request, 'main/buy.html', {'scheduled': scheduled, 'schedule_id': schedule_id})


def check(request, schedule_id):
    if request.method == 'POST':
        #checks = request.POST['checks']
        smth = request.POST.getlist('checks[]')
        scheduled = Schedule.objects.filter(pk=schedule_id)
        #checks = request.POST.getlist('checks')
        return render(request, 'main/check.html', {'scheduled': scheduled, 'schedule_id': schedule_id, 'checks': smth})


def seat_select(request):
    pass


def now_showing(request):
    scheduled = Schedule.objects.all().order_by('date')
    return render(request, 'main/now_showing.html', {'scheduled': scheduled})


"""
def add_movie(request):
    films = Movies.objects.all().filter()
    hall = Hall.objects.all().filter()
    time = TimeSlot.objects.all().filter()
    return render(request, 'main/add_movie.html', {'films': films, 'halls': hall, 'time': time})
"""
