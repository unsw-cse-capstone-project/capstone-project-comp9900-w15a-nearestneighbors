# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Movie(models.Model):
    mid = models.AutoField(primary_key=True, blank=True)
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    region = models.TextField(blank=True, null=True)
    released_date = models.TextField(blank=True, null=True)
    director = models.ForeignKey('Person', models.DO_NOTHING, blank=True, null=True)
    votecount = models.ForeignKey('Review', models.DO_NOTHING, db_column='votecount', blank=True, null=True, related_name='movie2review_votecount')
    rating = models.ForeignKey('Review', models.DO_NOTHING, db_column='rating', blank=True, null=True, related_name='movie2review_rating')

    class Meta:
        managed = False
        db_table = 'Movie'


class MoviePosters(models.Model):
    movieid = models.ForeignKey(Movie, models.DO_NOTHING, db_column='movieID', blank=True, null=True)  # Field name made lowercase.
    poster = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Movie_Posters'


class Cast(models.Model):
    castid = models.ForeignKey('Person', models.DO_NOTHING, db_column='castID', blank=True, null=True)  # Field name made lowercase.
    movieid = models.ForeignKey(Movie, models.DO_NOTHING, db_column='movieID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cast'


class MovieGenre(models.Model):
    movieid = models.ForeignKey(Movie, models.DO_NOTHING, db_column='movieID', blank=True, null=True)  # Field name made lowercase.
    genre_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_genre'


class Person(models.Model):
    pid = models.AutoField(primary_key=True, blank=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person'


class Review(models.Model):
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userID', blank=True, null=True)  # Field name made lowercase.
    movieid = models.ForeignKey(Movie, models.DO_NOTHING, db_column='movieID', blank=True, null=True)  # Field name made lowercase.
    review_comment = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)
    votecount = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review'


class User(models.Model):
    uid = models.AutoField(primary_key=True, blank=True)
    name = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    profile_photo = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class UserBannedList(models.Model):
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userID', blank=True)  # Field name made lowercase.
    banned_user_id = models.IntegerField(db_column='banned_user_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_banned_list'


class WatchHistory(models.Model):
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userID', blank=True, null=True)  # Field name made lowercase.
    movieid = models.ForeignKey(Movie, models.DO_NOTHING, db_column='movieID', blank=True, null=True)  # Field name made lowercase.
    watch_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'watch_history'


class WishList(models.Model):
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userID', blank=True, null=True)  # Field name made lowercase.
    movieid = models.ForeignKey(Movie, models.DO_NOTHING, db_column='movieID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wish_list'
