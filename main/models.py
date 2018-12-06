from django.db import models
from django.contrib.auth.models import User
import datetime


class Movies(models.Model):
    name = models.TextField(max_length=200)
    genre = models.TextField(null=True)
    language = models.TextField(null=True)
    length = models.IntegerField(null=True)
    rating = models.IntegerField()

    def __str__(self):
        return self.name


class Hall(models.Model):
    name = models.TextField(max_length=20, null=True)
    capacity = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    movie = models.ForeignKey(Movies)
    hall = models.ForeignKey(Hall)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    date = models.DateField(null=True)
    price = models.DecimalField(max_digits=6, decimal_places=0, null=True)

    def __str__(self):
        beautified = '  |  '.join([str(self.movie), str(self.hall), str(self.start_time),
                                   str(self.end_time), str(self.date)])
        return beautified


class Seat(models.Model):
    hall_id = models.ForeignKey(Hall, on_delete=models.CASCADE)
    row = models.IntegerField(null=True)
    seat = models.IntegerField(null=True)

    def __str__(self):
        beautified = '  |  '.join([str(self.row), str(self.seat)])
        return beautified


class Customers(models.Model):
    email =  models.TextField(max_length=50, null=True)
    phone_number = models.TextField(max_length=15, null=True)


class Order(models.Model):
    customer_id = models.ForeignKey(Customers,null=True)
    schedule_id = models.ForeignKey(Schedule, null=True)
    quantity = models.IntegerField(null=True)
    timestamp = models.TimeField(default=datetime.date.today())

class OrderedSeats(models.Model):
    order_id = models.ForeignKey(Order, null=True)
    schedule_id = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True)
    seat = models.ForeignKey(Seat, null=True)

class Tickets(models.Model):
    order_id = models.ForeignKey(Order, null=True)
