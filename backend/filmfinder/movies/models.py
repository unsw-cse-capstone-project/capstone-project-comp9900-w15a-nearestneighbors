from django.db import models
import datetime
from django.utils import timezone
# Create your models here.

class Person(models.Model):
    pid = models.AutoField(primary_key=True) # primary_key
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
        
    class Meta:
        ordering = ['name']

class Movie(models.Model):
    mid = models.AutoField(primary_key=True) # primary_key
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    region = models.CharField(max_length=50)
    released_date = models.DateTimeField('released date')
    poster = models.ImageField(upload_to='posters',blank = True, null = True)    #TODO
    director = models.ForeignKey(Person, on_delete=models.CASCADE)  #foreign key
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

#TODO
#class User(models.Model)



class Cast(models.Model):
    cast = models.ForeignKey(Person, on_delete=models.CASCADE)  #foreign key
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  #foreign key
    
    class Meta:
        unique_together=[["cast","movie"]]

#TODO
#class Review(models.Model)
#class Watch_history(models.Model)
#class Wish_list(modesl.Model)

class Movie_genre(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)   #foreign key
    genre_type = models.CharField(max_length = 50)
    
    class Meta:
        unique_together=[["movie","genre_type"]]

#TODO
#class User_banned_list(models.Model)