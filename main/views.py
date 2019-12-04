from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Genres,Movies,Comments, Cinemas,CinemaRating, UserRatings, CinemaComments, Schedules, Halls, Seats, Customers, Orders, OrderedSeats, Tickets
from django.contrib.auth.decorators import login_required
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def movies(request):
    movies_list = Movies.objects.all().order_by('-id')
    paginator = Paginator(movies_list, 3)

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
    movie = Movies.objects.get(pk=movie_id)
    comments = Comments.objects.filter(movie = movie).order_by('-created_at')
    context = {
        'movie': movie,
        'comments': comments
    }

    if request.method == 'POST':
        if request.POST['comment']:
            comment = Comments()
            comment.movie = movie
            comment.user = request.user
            comment.text = request.POST['comment']
            comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'main/movie_details.html', context)

@login_required
def edit_comment(request, comment_id):
    comment = Comments.objects.get(pk=comment_id)
    if request.user != comment.user:
        return redirect('movies')

    context = {
        'comment': comment
    }
    next = request.POST.get('next', '/')
    if request.method == 'POST':
        if request.POST['comment']:
            comment.text = request.POST['comment']
            comment.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

    return render(request, 'main/edit_comment.html', context)

def delete_comment(request, comment_id):
    comment = Comments.objects.get(pk=comment_id)
    if request.user != comment.user:
        return redirect('movies')
    comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def now_showing(request):
    scheduled = Schedules.objects.all().order_by('date')
    return render(request, 'main/now_showing.html', {'scheduled': scheduled})

def cinema_schedule(request, cinema_id):
    cinema = Cinemas.objects.get(id=cinema_id)
    schedules = Schedules.objects.filter(hall__cinema=cinema_id).order_by('date')
    context = {
        'cinema': cinema,
        'schedules': schedules
    }
    return render(request, 'main/cinema_schedule.html', context)

def buy(request, schedule_id):
    if request.method == 'POST':
        ordered_seats = OrderedSeats.objects.values_list('seat', flat=True).filter(order_id__schedule_id=schedule_id)
        not_free = []
        ordered = []
        for i in ordered_seats:
            seats = Seats.objects.values_list('row', 'seat').filter(pk=i)
            not_free.append(seats[0])
        for j in not_free:
            ordered.append(str(j[0])+ '-' + str(j[1]))
        request.session['ordered'] = ordered
        return render(request, 'main/buy_final.html', {'schedule_id': schedule_id, 'ord':ordered})
    else:
        scheduled = Schedules.objects.filter(pk=schedule_id)
        return render(request, 'main/buy.html', {'scheduled': scheduled, 'schedule_id': schedule_id})


def check(request, schedule_id):
    checks = request.POST.getlist('checks[]')
    if len(checks) == 0:
        error = 'You should select at least 1 seat !!!'
        ordered = request.session.get('ordered')

        return render(request, 'main/buy_final.html', {'schedule_id': schedule_id, 'ord':ordered, 'error':error})

    checks = map(str, checks)
    checks = list(checks)
    scheduled = Schedules.objects.filter(pk=schedule_id)
    price = Schedules.objects.values_list('price', flat=True).get(pk=schedule_id)
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
    #Creates new customer if not exist
    customers, created = Customers.objects.get_or_create(email=email, phone_number=phone)
    if not created:
        customers.save()

    schedule_id = Schedules.objects.get(pk=schedule_id_)
    customer = Customers.objects.get(pk=customers.id)
    order = Orders(customer_id=customer, schedule_id=schedule_id, quantity=quantity, timestamp=datetime.datetime.now())
    order.save()

    for i in checks:
        full_seat =  i.split('-')

        ord = Orders.objects.get(pk=order.id)
        seat = Seats.objects.get(hall_id=schedule_id.hall, row = full_seat[0], seat=full_seat[1])
        ordered_seats = OrderedSeats(order_id=ord, seat=seat)
        ordered_seats.save()

        ticket = Tickets(order_id=ord, seat=seat)
        ticket.save()

        tickets = Tickets.objects.all().filter(order_id=ord)

    return render(request, 'main/checkout.html', {'price': price, 'quantity': quantity*'x', 'checks': checks, 'id': order.id, 'movie':schedule_id, 'tickets':tickets })

def cinemas(request):
    cinemas = Cinemas.objects.all()
    context = {
        'cinemas': cinemas
    }

    return render(request, 'main/cinemas.html', context)

def cinema_about(request, cinema_id):
    cinema = Cinemas.objects.get(id=cinema_id)
    comments = CinemaComments.objects.filter(cinema = cinema).order_by('-created_at')
    rating = UserRatings.objects.filter(user=request.user, cinema=cinema_id).count()

    if request.method == 'POST':
        if request.POST['comment']:
            comment = CinemaComments()
            comment.cinema = cinema
            comment.user = request.user
            comment.text = request.POST['comment']
            comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {
        'cinema': cinema,
        'comments': comments,
        'rating': rating
    }

    return render(request, 'main/cinema_about.html', context)

def rate_cinema(request, cinema_id):
    cinema = Cinemas.objects.get(id=cinema_id)

    if request.method == 'POST':
        rating = UserRatings()
        rating.cinema = cinema
        rating.user = request.user
        rating.rating = request.POST['rating']
        rating.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required
def edit_cinema_comment(request, comment_id):
    comment = CinemaComments.objects.get(pk=comment_id)
    if request.user != comment.user:
        return redirect('movies')

    context = {
        'comment': comment
    }
    next = request.POST.get('next', '/')
    if request.method == 'POST':
        if request.POST['comment']:
            comment.text = request.POST['comment']
            comment.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

    return render(request, 'main/edit_cinema_comment.html', context)

def delete_cinema_comment(request, comment_id):
    comment = CinemaComments.objects.get(pk=comment_id)
    if request.user != comment.user:
        return redirect('movies')
    comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def create_seats(request):
    # red_hall = Halls.objects.get(name='Red')
    # blue_hall = Halls.objects.get(name='Blue')
    # big_hall = Halls.objects.get(name='Hall 1')
    # for s in range(1,7):
    #     for r in range(1,11):
    #         seats = Seats()
    #         seats.hall_id = big_hall
    #         seats.row = r
    #         seats.seat = s
    #         seats.save()

    return redirect('movies')
