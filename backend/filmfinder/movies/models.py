from django.db import models
from login.models import User
from django.utils import timezone
# Create your models here.

# a custom CharField that treats all letters as lower case
class lower_CharField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(lower_CharField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()

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
    description = models.CharField(max_length=1000)
    region = models.CharField(max_length=50)
    released_date = models.DateTimeField('released date')
    poster = models.ImageField(upload_to='../movies/posters',blank = True, null = True)    #TODO
    director = models.ForeignKey(Person, on_delete=models.CASCADE)  #foreign key
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    votecount = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

#TODO
#class User(models.Model)



class Cast(models.Model):
    cast = models.ForeignKey(Person, on_delete=models.CASCADE)  #foreign key
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  #foreign key
    
    def __str__(self):
        return self.cast.name + ' is one of cast for movie: ' + self.movie.name
    class Meta:
        unique_together=[["cast","movie"]]

#TODO
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='review')
    review_comment = models.TextField(max_length=1000)
    rating_number = models.FloatField()
    date = models.DateTimeField()
    
    def __str__(self):
        return self.user.name + ' has a review for movie: ' + self.movie.name
    
    class Meta:
        unique_together=[["user","movie"]]

#class Watch_history(models.Model)
class Wish_list(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.name + "'s wishlist contains " + self.movie.name
    
    class Meta:
        unique_together=[["user","movie"]]

class Movie_genre(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE, related_name='genre')   #foreign key
    genre_type = models.CharField(max_length = 50)
    
    def __str__(self):
        return self.movie.name + ' has genre_type: ' + self.genre_type
    
    class Meta:
        unique_together=[["movie","genre_type"]]

#TODO
class User_banned_list(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'banned_user_set')
    banned_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'users_banned_this_user_set')
    def __str__(self):
        return self.user.name + ' bans ' + self.banned_user.name
    class Meta:
        unique_together=[["user","banned_user"]]
