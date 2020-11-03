from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from . import models
from django.db.models import Avg
import simplejson
from django.http import JsonResponse
from django.core import serializers
import pdb

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


# Create your views here.
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
    data = {}
    data['success'] = False
    data['msg'] = ''
    data['movie'] = []
    if request.method == 'GET':
        try:
            req = simplejson.loads(request.body)
            key_words = req['movie_id'].strip()
        except:
            key_words = request.GET.get('movie_id')
        # Check if input is empty
        if not key_words:
            data['msg'] = 'movie_id is required'
            return JsonResponse(data)
        
        #else input is not empty
        try:
            movie_obj = models.Movie.objects.get(mid = key_words)
        except ValueError:
            data['msg'] = 'movie_id must be a integer'
        except ObjectDoesNotExist:
            data['msg'] = 'The movie you are looking for does not exist'
        else:
            data['success'] = True
            data['msg'] = 'found movie with movie_id: ' + str(key_words)
            data['movie'].append(movie_to_dict(movie_obj))
        finally:
            return JsonResponse(data)
    else:
        data['msg'] = "please use GET"
        return JsonResponse(data)
            

def search_by_name_view(request):
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

