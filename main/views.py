from django.shortcuts import render, get_object_or_404
from .models import Schedule, Movies, Hall, Seat, Customers, Order
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
    checks = request.POST.getlist('checks[]')
    scheduled = Schedule.objects.filter(pk=schedule_id)
    price = Schedule.objects.values_list('price', flat=True).get(pk=schedule_id)
    quantity = len(checks)
    amount = price * quantity

    return render(request, 'main/check.html', {'scheduled': scheduled,
                    'schedule_id': schedule_id, 'checks': checks,
                     'amount': amount, 'quantity': quantity, 'range': range(quantity)})



def checkout(request, schedule_id):
    email = request.POST.get('email')
    phone = request.POST.get('phone_number')
    customers = Customers(email=email, phone_number=phone)
    customers.save()

    return render(request, 'main/checkout.html')




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
