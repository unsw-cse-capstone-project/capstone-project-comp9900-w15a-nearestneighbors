from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Person)
admin.site.register(models.Movie)
admin.site.register(models.Cast)
admin.site.register(models.Movie_genre)