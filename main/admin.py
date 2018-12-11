from django.contrib import admin
from . import models

admin.site.register(models.Movies)
admin.site.register(models.Hall)
admin.site.register(models.Seat)
admin.site.register(models.Schedule)
admin.site.register(models.Tickets)
admin.site.register(models.Order)
admin.site.register(models.OrderedSeats)
admin.site.register(models.Customers)
admin.site.register(models.Genre)
