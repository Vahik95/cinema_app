from django.contrib import admin
from . import models

admin.site.register(models.Genres)
admin.site.register(models.Movies)
admin.site.register(models.Comments)
admin.site.register(models.Halls)
admin.site.register(models.Seats)
admin.site.register(models.Schedules)
admin.site.register(models.Tickets)
admin.site.register(models.Orders)
admin.site.register(models.OrderedSeats)
admin.site.register(models.Customers)
admin.site.register(models.Cinemas)
admin.site.register(models.CinemaComments)
admin.site.register(models.CinemaRating)
admin.site.register(models.UserRatings)
