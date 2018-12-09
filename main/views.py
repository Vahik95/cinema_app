from django.shortcuts import render, get_object_or_404, redirect
from .models import Schedule, Movies, Hall, Seat, Customers, Order, OrderedSeats, Tickets
from django.contrib.auth.decorators import login_required
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


"""
def movies(request):
    films = Movies.objects.all()
    return render(request, 'main/movies.html', {'films': films})
"""

def movies(request):
    movies_list = Movies.objects.all()
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


def now_showing(request):
    scheduled = Schedule.objects.all().order_by('date')
    return render(request, 'main/now_showing.html', {'scheduled': scheduled})


def buy(request, schedule_id):
    if request.method == 'POST':
        ordered_seats = OrderedSeats.objects.values_list('seat', flat=True).filter(schedule_id=schedule_id)
        not_free = []
        ordered = []
        for i in ordered_seats:
            seats = Seat.objects.values_list('row', 'seat').filter(pk=i)
            not_free.append(seats[0])
        for j in not_free:
            ordered.append(str(j[0])+ '-' + str(j[1]))
        request.session['ordered'] = ordered
        return render(request, 'main/buy_final.html', {'schedule_id': schedule_id, 'ord':ordered})
    else:
        scheduled = Schedule.objects.filter(pk=schedule_id)
        return render(request, 'main/buy.html', {'scheduled': scheduled, 'schedule_id': schedule_id})


def check(request, schedule_id):
    checks = request.POST.getlist('checks[]')
    if len(checks) == 0:
        error = 'You should select at least 1 seat !!!'
        ordered = request.session.get('ordered')

        return render(request, 'main/buy_final.html', {'schedule_id': schedule_id, 'ord':ordered, 'error':error})

    checks = map(str, checks)
    checks = list(checks)
    scheduled = Schedule.objects.filter(pk=schedule_id)
    price = Schedule.objects.values_list('price', flat=True).get(pk=schedule_id)
    quantity = len(checks)
    amount = price * quantity

    request.session['checks'] = checks
    request.session['schedule_id'] = int(schedule_id)
    request.session['price'] = int(price)
    request.session['quantity'] = int(quantity)
    request.session['amount'] = int(amount)

    return render(request, 'main/check.html', {'scheduled': scheduled,
                    'schedule_id': schedule_id, 'checks': checks,
                         'amount': amount, 'quantity': quantity, 'range': range(quantity)})


def checkout(request, schedule_id):
    schedule_id_ = request.session.get('schedule_id')
    checks = request.session.get('checks')
    price = request.session.get('price')
    quantity = request.session.get('quantity')

    email = request.POST.get('email')
    phone = request.POST.get('phone_number')
    customers = Customers(email=email, phone_number=phone)
    customers.save()

    schedule_id = Schedule.objects.get(pk=schedule_id_)
    customer = Customers.objects.get(pk=customers.id)
    order = Order(customer_id=customer, schedule_id=schedule_id, quantity=quantity, timestamp=datetime.datetime.now())
    order.save()

    for i in checks:
        full_seat =  i.split('-')

        ord = Order.objects.get(pk=order.id)
        seat = Seat.objects.get(hall_id=schedule_id.hall, row = full_seat[0], seat=full_seat[1])
        ordered_seats = OrderedSeats(order_id=ord, schedule_id=schedule_id, seat=seat)
        ordered_seats.save()

        ticket = Tickets(order_id=ord, schedule_id=schedule_id, seat=seat, customer_id=customers)
        ticket.save()

        tickets = Tickets.objects.all().filter(order_id=ord)

    return render(request, 'main/checkout.html', {'price': price, 'quantity': quantity*'x', 'checks': checks, 'id': order.id, 'movie':schedule_id, 'tickets':tickets })



"""
def add_movie(request):
    films = Movies.objects.all().filter()
    hall = Hall.objects.all().filter()
    time = TimeSlot.objects.all().filter()
    return render(request, 'main/add_movie.html', {'films': films, 'halls': hall, 'time': time})
"""
