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
     'cast': ['test_actor1', 'test_actor2'],
     'average_rating': 4.5
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
    movie['average_rating'] = models.Review.objects.filter(movie_id__exact=movie['mid']).aggregate(Avg('rating_number', distinct=True))['rating_number__avg']
    if movie['average_rating'] is not None:
                movie['average_rating'] = round(movie['average_rating'], 1)
    
    return movie

def review_to_dict(review_obj):
    '''
    convert review_obj to a dict,
    containing user_id, user_name, movie_id, movie_name, review_comment, rating_number, date
    
    e.g.
    {
        'user_id': 4,
        'user_name': '4@4.4',
        'movie_id': 5,
        'movie_name': 'Avengers: Age of Ultron',
        'review_comment': "Marvel's The Avengers (2012) is an awesome movie.",
        'rating_number': 5.0,
        'date': datetime.datetime(2013, 2, 3, 6, 37, 24, tzinfo=<UTC>)
    }

    '''
    review = {}
    review['user_id'] = review_obj.user.uid
    review['user_name'] = review_obj.user.name
    review['movie_id'] = review_obj.movie.mid
    review['movie_name'] = review_obj.movie.name
    review['review_comment'] = review_obj.review_comment
    review['rating_number'] = review_obj.rating_number
    review['date'] = review_obj.date
    return review
    

def movie_detail_to_dict(movie_obj):
    '''
    convert movie_object to a dict containing
    mid, name, list of genre type, description, region, released_date, director_name, poster image path, list of cast name, list of reviews
    
    e.g.
    {
        'mid': 4,
        'name': 'The Avengers',
        'genre': ['Action', 'Adventure', 'Science fiction'],
        'description': "Marvel's The Avengers[6] (classified under the name .....",
        'region': 'United States',
        'released_date': datetime.datetime(2012, 5, 4, 12, 0, tzinfo=<UTC>),
        'director': 'Joss Whedon',
        'poster': '../movies/posters/The_Avengers_2012_film_poster.jpg',
        'cast': [
                    'Robert Downey Jr.',
                    'Chris Evans',
                    'Mark Ruffalo',
                    'Chris Hemsworth',
                    'Scarlett Johansson',
                    'Jeremy Renner',
                    'Tom Hiddleston'
                ],
        'average_rating': 4.5,
        'reviews':[
                    {
                        'user_name': '6@6.6',
                        'review_comment': 'I was lucky enough to attend the Marve.....',
                        'rating_number': 4.5,
                        'date': datetime.datetime(2018, 4, 11, 6, 41, 19, tzinfo=<UTC>)
                    },
                    {
                        'user_name': '5@5.5',
                        'review_comment': "'Avengers Assemble' ('The Avengers') is a truly enjoyable superhero film that ....",
                        'rating_number': 5.0,
                        'date': datetime.datetime(2015, 11, 4, 6, 40, 34, tzinfo=<UTC>)
                    },
                    {
                        'user_name': '7@7.7',
                        'review_comment': "I just saw the early screening for San Diego through the top 10 cities on facebook who got them.....",
                        'rating_number': 4.7,
                        'date': datetime.datetime(2012, 12, 30, 6, 41, 53, tzinfo=<UTC>)
                    }
                ]
    }

    '''
    movie_dict = movie_to_dict(movie_obj)
    movie_dict['reviews'] = []
    for review_obj in movie_obj.review_set.all().order_by('-date')[:5]:
        review_dict = review_to_dict(review_obj)
        del review_dict['user_id']
        del review_dict['movie_id']
        del review_dict['movie_name']
        movie_dict['reviews'].append(review_dict)
    return movie_dict
    

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
            data['movie'].append(movie_detail_to_dict(movie_obj))
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

        # Get movies that keywords is or is a substring of movie names
        movie_list = list(models.Movie.objects.filter(name__icontains=key_words).values('mid', 'name', 'released_date', 'poster'))
        for movie in movie_list:
            movie['rating'] = models.Review.objects.filter(movie_id__exact=movie['mid']).aggregate(Avg('rating_number', distinct=True))['rating_number__avg']
            if movie['rating'] is not None:
                movie['rating'] = round(movie['rating'], 1)
        # pdb.set_trace()
        data = {
            'success': True,
            'result': []
        }
        # data['result'].append(serializers.serialize('python', movie_list))
        data['result'] = list(movie_list)
        return JsonResponse(data)
        # pdb.set_trace()

    return

