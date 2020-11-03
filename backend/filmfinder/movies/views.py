from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from . import models    #models in movies App
import login.models # models in login App
from django.db.models import Avg
import simplejson
import datetime
from django.utils import timezone
from django.http import JsonResponse
from django.core import serializers
import pdb
import re


'''internal function'''
def movie_to_dict(movie_obj):
    '''
    convert movie_object to a dict containing
    mid, name, list of genre type, description, region, released_date, director_name, poster image path, list of cast name
    
    e.g.
    {'mid': 1,
     'name': 'test_movie1',
     'genre': ['test_genre1', 'test_genre12', 'test_genre3'],
     'description': 'test_movie1_description',
     'region': 'US',
     'released_date': datetime.datetime(2020, 10, 30, 9, 37, 52, tzinfo=<UTC>),
     'director': 'test_director1',
     'poster': '../movies/posters/壁纸.jpg',
     'cast': ['test_actor1', 'test_actor2']
    }
    '''
    movie = {} 
    movie['mid'] = movie_obj.mid 
    movie['name'] = movie_obj.name
    movie['genre'] = [movie_genre_obj.genre_type for movie_genre_obj in movie_obj.movie_genre_set.all()]
    movie['description'] = movie_obj.description 
    movie['region'] = movie_obj.region 
    movie['released_date'] = movie_obj.released_date 
    movie['director'] = movie_obj.director.name 
    movie['poster'] = str(movie_obj.poster) 
    movie['cast'] = [cast_obj.cast.name for cast_obj in movie_obj.cast_set.all()]
    
    return movie

'''APIs'''
def movie_list_view(request):
    '''
    return all movies detail by calling 'movie_to_dict' function for all movie objects in database 
    and return in Json from
    '''
    data = {}
    data['success'] = False
    data['movies'] = []
    if request.method == 'GET':
        data['success'] = True
        movie_obj_list = models.Movie.objects.order_by('name')[:]
        for movie_obj in movie_obj_list:
            data['movies'].append(movie_to_dict(movie_obj))
    return JsonResponse(data)
    
def detail_view(request):
    '''
    get a movie detail by giving movie_id.
    the input json has this format:
    {
        "movie_id": "some movie id here, must be a positive integer"
    }
    '''
    data = {}
    data['success'] = False
    data['msg'] = ''
    data['movie'] = []
    if request.method == 'GET':
        try:
            req = simplejson.loads(request.body)
            movie_id = req['movie_id'].strip()
        except:
            movie_id = request.GET.get('movie_id')
        # Check if input is empty
        if movie_id == None:
            data['msg'] = 'movie_id is required'
            return JsonResponse(data)
        #else input is not empty
        
        #check if movie_id is a positive integer
        try:
            movie_id = int(movie_id)
            if not (movie_id > 0):
                data['msg'] = 'movie_id must be a positive integer'
                return JsonResponse(data)
        except:
            data['msg'] = 'movie_id must be a positive integer'
            return JsonResponse(data)
        
        try:
            movie_obj = models.Movie.objects.get(mid = movie_id)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have movie with movie_id: ' + str(movie_id)
            return JsonResponse(data)
        else:
            data['success'] = True
            data['msg'] = 'found movie with movie_id: ' + str(movie_id)
            data['movie'].append(movie_to_dict(movie_obj))
            return JsonResponse(data)
            
    else:
        data['msg'] = "please use GET"
        return JsonResponse(data)
 
def new_review_view(request):
    '''
    a view function that create a new Review tuple
    the input json has this format:
    {
        "movie_id": "some movie id here, must be a positive integer",
        "review_comment": "some comment here, must be a string",
        "rating_number": "some rating number here, must be a positive number",
    }
    '''
    data = {}
    data['success'] = False
    data['msg'] = ''
    if request.method == 'POST':
        # Check if the user has already logged in.
        # If user has not logged in, return an error msg to frontend.
        # If user has logged in, let user create a new review
        if not request.session.get('login_flag', None):
            data['msg'] = 'user does not log in'
            return JsonResponse(data)
        #else use is logged in
        user_name = request.session.get('name', None)
        # return user_obj by user_name from login.models.User database
        try:
            user_obj = login.models.User.objects.get(name = user_name)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have user: ' + str(user_name)
            return JsonResponse(data)
        
        req = simplejson.loads(request.body)
        movie_id = req.get('movie_id', None)
        review_comment = req.get('review_comment', None)
        rating_number = req.get('rating_number', None)
        
        #check if either movie_id, review_comment, rating_number, is empty
        if movie_id == None or review_comment == None or rating_number == None:
            data['msg'] = 'movie_id, review_comment, rating_number are required'
            return JsonResponse(data)
        
        # check movie_id is a positive integer and rating_number is a positive number
        try:
            movie_id = int(movie_id)
            rating_number = float(rating_number)
            if not (movie_id > 0 and rating_number >= 0):
                data['msg'] = 'movie_id must be a positive integer, ' + \
                              'review_comment must be a string, ' + \
                              'rating_number must be a positive number'
                return JsonResponse(data)
        except:
            data['msg'] = 'movie_id must be a positive integer, ' + \
                              'review_comment must be a string, ' + \
                              'rating_number must be a positive number'
            return JsonResponse(data)
    
        # return movie_obj by movie_id from models.Movie database
        try:
            movie_obj = models.Movie.objects.get(mid = movie_id)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have movie with movie_id: ' + str(movie_id)
            return JsonResponse(data)
        
        date = datetime.datetime.now(timezone.utc)
        
        try:
            models.Review.objects.create(user = user_obj, movie = movie_obj, review_comment = review_comment, rating_number = rating_number, date = date)
        except:
            data['msg'] = 'each user can only leave one review for a movie, but reviews are editable'
            return JsonResponse(data)
        else:
            data['success'] = True
            data['msg'] = 'successfully create a new review'
            return JsonResponse(data)
    else:
        data['msg'] = 'please use POST'
        return JsonResponse(data)


def search_view(request):
    if request.method == 'GET':
        # key_words = request.GET.get('search')
        try:
            req = simplejson.loads(request.body)
            key_words = req['search'].strip()
        except:
            key_words = request.GET.get('search')
        # Check if input is empty
        if not key_words:
            data = {
                'success': False,
                'msg': 'empty input'
            }
            return JsonResponse(data)

        data = {
            'success': True,
            'result': []
        }

        key_words_list = key_words.split(' ')

        by_genre = []
        by_director = []
        by_time = []
        by_region = []

        all_genres = ['action', 'animation', 'comedy', 'crime', 'documentary', 'drama', 'fantacy', 'horror', 'kids', 'family', 'mystery', 'romance', 'science', 'fiction']

        # Get movies that keyword is or is a substring of movie names
        by_name = list(models.Movie.objects.filter(name__icontains=key_words).values_list('mid', flat=True))

        for word in key_words_list:

            if word:
                # Get movies that keyword is or is a substring of genres
                if word.lower() in all_genres:
                    id_list = list(models.Movie_genre.objects.filter(genre_type__icontains=word).values_list('movie_id', flat=True).distinct())
                    by_genre.extend(id_list)

                # Get movies that keyword is or is a substring of a director's name
                pid_list = list(models.Person.objects.filter(name__icontains=word).values_list('pid', flat=True).distinct())
                if pid_list:
                    id_list = list(models.Movie.objects.filter(director_id__in=pid_list).values_list('mid', flat=True).distinct())
                    by_director.extend(id_list)

                # Get movies that keyword is a time
                if re.findall(r'[1-2][0-9][0-9][0-9]', word):
                    id_list = list(models.Movie.objects.filter(released_date__year=word).values_list('mid', flat=True).distinct())
                    by_time.extend(id_list)

                # Get movies that keyword is a region
                id_list = list(models.Movie.objects.filter(region__icontains=word).values_list('mid', flat=True))
                by_region.extend(id_list)

        if by_name:
            result_id_list = by_name + by_genre + by_director + by_time + by_region
        else:
            set_list = [set(by_genre), set(by_director), set(by_time), set(by_region)]
            set_list = [s for s in set_list if len(s) != 0]
            result_id_list = set.intersection(*set_list)

        # Get and calculate latest average ratings
        movie_list = list(models.Movie.objects.filter(mid__in=result_id_list).values('mid', 'name', 'released_date', 'poster'))
        for movie in movie_list:
            movie['rating'] = models.Review.objects.filter(movie_id__exact=movie['mid']).aggregate(Avg('rating_number', distinct=True))['rating_number__avg']
            if movie['rating'] is not None:
                movie['rating'] = round(movie['rating'], 1)

        # Sort results based on ratings.
        # If two are the same then sort results alphabetically.
        data['result'] = sorted(list(movie_list), key=lambda x: (-x['rating'], x['name']))
        return JsonResponse(data)

    return

