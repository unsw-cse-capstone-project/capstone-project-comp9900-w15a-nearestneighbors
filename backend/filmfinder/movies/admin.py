from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Person)
admin.site.register(models.Movie)
admin.site.register(models.Cast)
admin.site.register(models.Movie_genre)
admin.site.register(models.Review)
admin.site.register(models.User_banned_list)
admin.site.register(models.Wish_list)