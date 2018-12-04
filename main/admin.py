from django.contrib import admin
from . import models

admin.site.register(models.Movies)
admin.site.register(models.Hall)
admin.site.register(models.Seat)
admin.site.register(models.Schedule)