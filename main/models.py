from django.db import models
from django.contrib.auth.models import User


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
        beautified = '  |  '.join([self.name, str(self.capacity)])
        return beautified


class Seat(models.Model):
    hall_id = models.ForeignKey(Hall, on_delete=models.CASCADE)
    row = models.IntegerField(null=True)
    seat = models.IntegerField(null=True)

    def __str__(self):
        beautified = '  |  '.join([str(self.row), str(self.seat)])
        return beautified


class Schedule(models.Model):
    movie = models.ForeignKey(Movies)
    hall = models.ForeignKey(Hall)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    date = models.DateField(null=True)

    def __str__(self):
        beautified = '  |  '.join([str(self.movie), str(self.hall), str(self.start_time),
                                   str(self.end_time), str(self.date)])
        return beautified
