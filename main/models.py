from django.db import models
from django.contrib.auth.models import User
import datetime


class Genres(models.Model):
    name = models.TextField(max_length=50)

    def __str__(self):
        return self.name


class Movies(models.Model):
    name = models.TextField(max_length=200)
    language = models.TextField(null=True)
    description = models.TextField(max_length=1500, null=True)
    length = models.IntegerField(null=True)
    rating = models.IntegerField()
    genre = models.ManyToManyField(Genres)
    image = models.ImageField(upload_to='media/', blank=True)

    def __str__(self):
        return self.name


class Halls(models.Model):
    name = models.TextField(max_length=20, primary_key=True, null=False)
    capacity = models.IntegerField(null=True)

    def __str__(self):
        return self.name


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


class Seats(models.Model):
    hall_id = models.ForeignKey(Halls, null=True, on_delete=models.CASCADE)
    row = models.IntegerField(null=True)
    seat = models.IntegerField(null=True)

    def __str__(self):
        beautified = '  |  '.join([str(self.row), str(self.seat)])
        return beautified


class Customers(models.Model):
    email =  models.TextField(max_length=50, null=True)
    phone_number = models.TextField(max_length=15, null=True)

    def __str__(self):
        return str(self.email) + '   |   ' + str(self.phone_number)


class Orders(models.Model):
    customer_id = models.ForeignKey(Customers,null=True)
    schedule_id = models.ForeignKey(Schedules, null=True)
    quantity = models.IntegerField(null=True)
    timestamp = models.TimeField(default=datetime.date.today())

    def __str__(self):
        return str(self.customer_id) + '   |   ' + str(self.timestamp)


class OrderedSeats(models.Model):
    order_id = models.ForeignKey(Orders, null=True, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seats, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.seat)


class Tickets(models.Model):
    order_id = models.ForeignKey(Orders, null=True, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seats, null=True, on_delete=models.CASCADE)
