from django.db import models
from django.contrib.auth.models import User
import datetime


class Genres(models.Model):
    name = models.TextField(max_length=50)

    def __str__(self):
        return self.name


class Movies(models.Model):
    name = models.TextField(max_length=200)
    language = models.TextField(max_length=20,null=True)
    description = models.TextField(max_length=1500, null=True)
    length = models.IntegerField(null=True)
    rating = models.IntegerField()
    genre = models.ManyToManyField(Genres)
    image = models.ImageField(upload_to='media/', blank=True)

    def __str__(self):
        return self.name
