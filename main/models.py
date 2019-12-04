from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import datetime

class Genres(models.Model):
    name = models.TextField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Genres"


class Movies(models.Model):
    name = models.TextField(max_length=200)
    language = models.TextField(max_length=20, null=True)
    description = models.TextField(max_length=15000, null=True)
    length = models.IntegerField(null=True)
    rating = models.IntegerField()
    genre = models.ManyToManyField(Genres)
    image = models.ImageField(upload_to='media/', blank=True)
    imdb_link = models.TextField(max_length=400, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Movies"


class Comments(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = "Comments"


class Cinemas(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='media/',null=True, blank=True)
    address = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cinemas"

class CinemaComments(models.Model):
    cinema = models.ForeignKey(Cinemas, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = "CinemaComments"

class Halls(models.Model):
    cinema = models.ForeignKey(Cinemas, on_delete=models.CASCADE)
    name = models.TextField(max_length=20, primary_key=True, null=False)
    capacity = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Halls"


class Schedules(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    hall = models.ForeignKey(Halls, on_delete=models.CASCADE)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    date = models.DateField(null=True)
    price = models.DecimalField(max_digits=6, decimal_places=0, null=True)

    def __str__(self):
        beautified = '  |  '.join([str(self.movie), str(self.hall), str(self.start_time),
                                   str(self.end_time), str(self.date)])
        return beautified

    class Meta:
        verbose_name_plural = "Schedules"


class Seats(models.Model):
    hall_id = models.ForeignKey(Halls, null=True, on_delete=models.CASCADE)
    row = models.IntegerField(null=True)
    seat = models.IntegerField(null=True)

    def __str__(self):
        beautified = '  |  '.join([str(self.row), str(self.seat)])
        return beautified

    class Meta:
        verbose_name_plural = "Seats"



class Customers(models.Model):
    email =  models.TextField(max_length=50, null=True)
    phone_number = models.TextField(max_length=15, null=True)

    def __str__(self):
        return str(self.email) + '   |   ' + str(self.phone_number)

    class Meta:
        verbose_name_plural = "Customers"


class Orders(models.Model):
    customer_id = models.ForeignKey(Customers,null=True, on_delete=models.CASCADE)
    schedule_id = models.ForeignKey(Schedules, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    timestamp = models.TimeField(default=datetime.date.today())

    def __str__(self):
        return str(self.customer_id) + '   |   ' + str(self.timestamp)

    class Meta:
        verbose_name_plural = "Orders"

class OrderedSeats(models.Model):
    order_id = models.ForeignKey(Orders, null=True, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seats, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.seat)

    class Meta:
        verbose_name_plural = "OrderedSeats"



class Tickets(models.Model):
    order_id = models.ForeignKey(Orders, null=True, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seats, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Tickets"
