from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
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
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django_pandas.io import read_frame
import pandas as pd
import numpy as np


'''internal function'''
def get_banned_user_obj_list(user_obj):
    '''
    input is an user object, this function returns a list of user objects that were banned by the input user
    
    e.g.
    user 'pete@123.com' banned user 'holly@123.com' and user '1@1.1',
    
    user_obj = models.User.objects.get(name = 'pete@123.com')
    banned_user_obj_list = get_banned_user_obj_list(user_obj)
    
    then, 
    banned_user_obj_list == [user_obj('holly@123.com'), user_obj('1@1.1')]
    '''
    banned_user_obj_list = [user_banned_list_obj.banned_user for user_banned_list_obj in user_obj.banned_user_set.all()]
    return banned_user_obj_list
    

def movie_to_dict(movie_obj,request):
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
    
    # if the user has logged in
    if request.session.get('login_flag', None):
        user_name = request.session.get('name', None)
        # return user_obj by user_name from login.models.User database
        try:
            user_obj = login.models.User.objects.get(name = user_name)
        except ObjectDoesNotExist: # should never goes into this statement
            banned_user_obj_list = []
        else:
            banned_user_obj_list = get_banned_user_obj_list(user_obj)
        finally:
            movie['average_rating'] = models.Review.objects.filter(movie_id__exact=movie['mid'])\
                                      .exclude(user__in = banned_user_obj_list)\
                                      .aggregate(Avg('rating_number', distinct=True))['rating_number__avg']
    
    # else the user does not log in    
    else:
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
    

def movie_detail_to_dict(movie_obj,request,num_review):
    '''
    convert movie_object to a dict containing
    mid, name, list of genre type, description, region, released_date, director_name, poster image path, list of cast name, list of reviews
    
    note that if user has logged in, list of reviews will not include reviews from its block list.
    
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
    movie_dict = movie_to_dict(movie_obj,request)
    movie_dict['reviews'] = []
    
    # if the user has logged in
    if request.session.get('login_flag', None):
        user_name = request.session.get('name', None)
        # return user_obj by user_name from login.models.User database
        try:
            user_obj = login.models.User.objects.get(name = user_name)
        except ObjectDoesNotExist:
            review_obj_list = movie_obj.review_set.all()
        else:
            banned_user_obj_list = get_banned_user_obj_list(user_obj)
            review_obj_list = movie_obj.review_set.exclude(user__in = banned_user_obj_list)
            
    # else the user does not log in
    else:
        review_obj_list = movie_obj.review_set.all()
    
    
    for review_obj in review_obj_list.order_by('-date')[:num_review]:
        review_dict = review_to_dict(review_obj)
        del review_dict['user_id']
        del review_dict['movie_id']
        del review_dict['movie_name']
        movie_dict['reviews'].append(review_dict)
    return movie_dict
    

def update_movie_rating_record(movie_id, rating_number, operation):
    movie = models.Movie.objects.get(mid=movie_id)
    if operation == 'new':
        # Update the average_rating and votecount for the movie.
        movie.average_rating = (float(movie.average_rating) * float(movie.votecount) + rating_number) / (movie.votecount + 1)
        movie.votecount += 1
        movie.save()
    elif operation == 'delete':
        movie.average_rating = (float(movie.average_rating) * float(movie.votecount) - float(rating_number)) / (movie.votecount - 1)
        movie.votecount -= 1
        movie.save()
    elif operation == 'edit':
        movie.average_rating = float(movie.average_rating) + (float(rating_number) / movie.votecount)
        movie.save()


'''APIs'''
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

        all_genres = ['action', 'animation', 'comedy', 'crime', 'documentary', 'drama', 'fantacy', 'horror', 'kids',
                      'family', 'mystery', 'romance', 'science', 'fiction']

        # Get movies that keyword is or is a substring of movie names
        by_name = list(models.Movie.objects.filter(name__icontains=key_words).values_list('mid', flat=True))

        for word in key_words_list:

            if word:
                # Get movies that keyword is or is a substring of genres
                if word.lower() in all_genres:
                    id_list = list(models.Movie_genre.objects.filter(genre_type__icontains=word).values_list('movie_id',
                                                                                                             flat=True).distinct())
                    by_genre.extend(id_list)

                # Get movies that keyword is or is a substring of a director's name
                pid_list = list(
                    models.Person.objects.filter(name__icontains=word).values_list('pid', flat=True).distinct())
                if pid_list:
                    id_list = list(
                        models.Movie.objects.filter(director_id__in=pid_list).values_list('mid', flat=True).distinct())
                    by_director.extend(id_list)

                # Get movies that keyword is a time
                if re.findall(r'[1-2][0-9][0-9][0-9]', word):
                    id_list = list(
                        models.Movie.objects.filter(released_date__year=word).values_list('mid', flat=True).distinct())
                    by_time.extend(id_list)

                # Get movies that keyword is a region
                id_list = list(models.Movie.objects.filter(region__icontains=word).values_list('mid', flat=True))
                by_region.extend(id_list)

        if by_name:
            result_id_list = by_name + by_genre + by_director + by_time + by_region
        else:
            if not by_genre and not by_director and not by_region and not by_time:
                return JsonResponse(data)

            set_list = [set(by_genre), set(by_director), set(by_time), set(by_region)]
            set_list = [s for s in set_list if len(s) != 0]
            result_id_list = set.intersection(*set_list)

        # Get and calculate latest average ratings
        movie_list = list(
            models.Movie.objects.filter(mid__in=result_id_list).values('mid', 'name', 'released_date', 'poster', 'average_rating'))

        # Sort results based on ratings.
        # If two are the same then sort results alphabetically.
        if movie_list:
            data['result'] = sorted(list(movie_list), key=lambda x: (-x['average_rating'], x['name']))

        return JsonResponse(data)

    return


def movie_list_view(request):
    '''
    return all movies detail by calling 'movie_to_dict' function for all movie objects in database 
    and return in Json form
    
    request.method == 'GET'
    '''
    data = {}
    data['success'] = False
    data['movies'] = []
    if request.method == 'GET':
        data['success'] = True
        movie_obj_list = models.Movie.objects.order_by('name')[:]
        for movie_obj in movie_obj_list:
            data['movies'].append(movie_to_dict(movie_obj,request))
    return JsonResponse(data)


def detail_view(request):
    '''
    get a movie detail by giving movie_id.
    the input json has this format:
    {
        "movie_id": "some movie id here, must be a positive integer"
    }
    
    request.method == 'GET'
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
            movie_obj = models.Movie.objects.get(mid=movie_id)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have movie with movie_id: ' + str(movie_id)
            return JsonResponse(data)
        else:
            data['success'] = True
            data['msg'] = 'found movie with movie_id: ' + str(movie_id)
            data['movie'].append(movie_detail_to_dict(movie_obj, request, num_review=5))
            review_and_wishlist = []
            # Check if user has logged in
            if request.session.get('login_flag', None):
                try:
                    username = request.session['name']
                    uid = login.models.User.objects.get(name=username).uid
                except:
                    similar_list = similar_movie(movie_obj.name, [])

                review_ids = list(models.Review.objects.filter(user_id=uid).values_list('movie_id', flat=True))
                review_names = list(models.Movie.objects.filter(mid__in=review_ids).values_list('name', flat=True))
                wishlist_ids = list(models.Wish_list.objects.filter(user_id=uid).values_list('movie_id', flat=True))
                wishlist_names = list(models.Movie.objects.filter(mid__in=wishlist_ids).values_list('name', flat=True))
                names_list = np.random.choice(np.concatenate([review_names, wishlist_names]),
                                              len(review_names) + len(wishlist_names), replace=False)
            else:
                names_list = []
            similar_list = similar_movie(movie_obj.name, names_list)
            data['similar_movies'] = list(models.Movie.objects.filter(name__in=similar_list).values('mid', 'name', 'released_date', 'poster', 'average_rating'))
            return JsonResponse(data)
            
    else:
        data['msg'] = "please use GET"
        return JsonResponse(data)


def similar_movie(movie_title, names_list):
    df = read_frame(models.MovieFeatures.objects.all())
    count = CountVectorizer()
    count_matrix = count.fit_transform(df['bag_of_words'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    indices = pd.Series(df['title'])

    def recommend(title, cosine_sim=cosine_sim):
        recommended_movies = []
        idx = indices[indices == title].index[0]
        score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)
        top_10_indices = list(score_series.iloc[1:11].index)

        for i in top_10_indices:
            recommended_movies.append(list(df['title'])[i])

        return recommended_movies

    if names_list:
        similar_movies = []
        for name in names_list:
            similar_movies.extend(recommend(name))
        return similar_movies[:10]
    else:
        return recommend(movie_title)




def add_to_wishlist_view(request):
    '''
    add movie given by movie_id to user's wish_list.
    the input json has this format:
    {
        "movie_id": "some movie id here, must be a positive integer"
    }
    
    request.method == 'GET'
    '''
    data = {}
    data['success'] = False
    data['msg'] = ''
    if request.method == 'GET':
        # Check if the user has already logged in.
        # If user has not logged in, return an error msg to frontend.
        # If user has logged in, let user add movie to his/her wishlist
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
        
        try:
            models.Wish_list.objects.create(user = user_obj, movie = movie_obj)
        except IntegrityError:
            data['msg'] = 'movie already in wishlist'
            return JsonResponse(data)
        else:
            data['success'] = True
            data['msg'] = 'successfully insert movie to wishlist'
            return JsonResponse(data)
        
    else:
        data['msg'] = 'please use GET'
        return JsonResponse(data)


def my_wishlist_view(request):
    '''
    get all movies in wishlist of the current user
    input: No input
    
    request.method == 'GET'
    '''
    data = {}
    data['success'] = False
    data['msg'] = ''
    data['wishlist'] = []
    if request.method == 'GET':
        # Check if the user has already logged in.
        # If user has not logged in, return an error msg to frontend.
        # If user has logged in, let user view his/her wishlist
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
        
        data['success'] = True
        data['msg'] = 'successfully get wishlist of the current user'
        
        movie_id_list = list(models.Wish_list.objects.filter(user__exact = user_obj).order_by('movie').values_list('movie_id',flat = True))
        useful_keys = {'mid','name','region','released_date','average_rating','poster'}
        for mid in movie_id_list:
            movie_obj = models.Movie.objects.get(mid = mid)
            movie_dict = movie_to_dict(movie_obj,request)
            data['wishlist'].append({key:value for key,value in movie_dict.items() if key in useful_keys})
        
        return JsonResponse(data)
        
    else:
        data['msg'] = 'please use GET'
        return JsonResponse(data)
        

def remove_from_wishlist_view(request):
    '''
    remove movie given by movie_id from user's wish_list.
    the input json has this format:
    {
        "movie_id": "some movie id here, must be a positive integer"
    }
    
    request.method == 'GET'
    '''
    data = {}
    data['success'] = False
    data['msg'] = ''
    if request.method == 'GET':
        # Check if the user has already logged in.
        # If user has not logged in, return an error msg to frontend.
        # If user has logged in, let user remove movie from his/her wishlist
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
        
        try:
            models.Wish_list.objects.get(user = user_obj, movie = movie_obj).delete()
        except ObjectDoesNotExist:
            data['msg'] = "movie with movie_id: " + str(movie_id) + ' is not in wishlist'
            return JsonResponse(data)
        else:
            data['success'] = True
            data['msg'] = 'successfully remove movie from wishlist'
            return JsonResponse(data)
        
    else:
        data['msg'] = 'please use GET'
        return JsonResponse(data)


def add_to_bannedlist_view(request):
    '''
    add user, that the current user doesn't like, given by banned_user_id, to the current user's blacklist.
    the input json has this format:
    {
        "banned_user_id": "banned user, that you don't like, id here, must be a positive integer"
    }
    
    request.method == 'GET'
    '''
    data = {}
    data['success'] = False
    data['msg'] = ''
    if request.method == 'GET':
        # Check if the current user has already logged in.
        # If user has not logged in, return an error msg to frontend.
        # If user has logged in, let user add banned user he/she doesn't like, to his/her blacklist
        if not request.session.get('login_flag', None):
            data['msg'] = 'user does not log in'
            return JsonResponse(data)
        #else current use is logged in
        curr_user_name = request.session.get('name', None)
        # return curr_user_obj by curr_user_name from login.models.User database
        try:
            curr_user_obj = login.models.User.objects.get(name = curr_user_name)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have user: ' + str(curr_user_name)
            return JsonResponse(data)
        
        try:
            req = simplejson.loads(request.body)
            banned_user_id = req['banned_user_id'].strip()
        except:
            banned_user_id = request.GET.get('banned_user_id')
        # check if input is empty
        if banned_user_id == None:
            data['msg'] = 'banned_user_id is required'
            return JsonResponse(data)
        
        # else input is not empty
        # check if banned_user_id is a positive integer
        try:
            banned_user_id = int(banned_user_id)
            if not (banned_user_id > 0):
                data['msg'] = 'banned_user_id must be a positive integer'
                return JsonResponse(data)
        except:
            data['msg'] = 'banned_user_id must be a positive integer'
            return JsonResponse(data)
        
        try:
            banned_user_obj = login.models.User.objects.get(uid = banned_user_id)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have user with banned_user_id: ' + str(banned_user_id)
            return JsonResponse(data)
        
        if curr_user_obj.uid == banned_user_obj.uid:
            data['msg'] = 'user cannot add itself to its blacklist'
            return JsonResponse(data)
        
        try:
            models.User_banned_list.objects.create(user = curr_user_obj, banned_user = banned_user_obj)
        except IntegrityError:
            data['msg'] = 'banned_user_id: ' + str(banned_user_id) + ' already in blacklist'
            return JsonResponse(data)
        else:
            data['success'] = True
            data['msg'] = 'successfully insert banned_user_id: ' + str(banned_user_id) + ' into blacklist'
            return JsonResponse(data)
        
    else:
        data['msg'] = 'please use GET'
        return JsonResponse(data)


def my_bannedlist_view(request):
    '''
    get all users in bannedlist of the current user
    input: No input
    
    request.method == 'GET'
    '''
    data = {}
    data['success'] = False
    data['msg'] = ''
    data['bannedlist'] = []
    if request.method == 'GET':
        # Check if the user has already logged in.
        # If user has not logged in, return an error msg to frontend.
        # If user has logged in, let user view his/her blacklist
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
        
        data['success'] = True
        data['msg'] = 'successfully get blacklist of the current user'
        
        banned_user_obj_list = get_banned_user_obj_list(user_obj)
        data['bannedlist'] = [{"uid":banned_user_obj.uid, "name":banned_user_obj.name} for banned_user_obj in banned_user_obj_list]
        return JsonResponse(data)
        
    else:
        data['msg'] = 'please use GET'
        return JsonResponse(data)


def remove_from_bannedlist_view(request):
    '''
    remove banned_user given by banned_user_id from user's blacklist.
    the input json has this format:
    {
        "banned_user_id": "some banned_user_id, that you want to no longer block, must be a positive integer"
    }
    
    request.method == 'GET'
    '''
    data = {}
    data['success'] = False
    data['msg'] = ''
    if request.method == 'GET':
        # Check if the user has already logged in.
        # If user has not logged in, return an error msg to frontend.
        # If user has logged in, let user remove banned_user from his/her blacklist
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
        
        try:
            req = simplejson.loads(request.body)
            banned_user_id = req['banned_user_id'].strip()
        except:
            banned_user_id = request.GET.get('banned_user_id')
        # check if input is empty
        if banned_user_id == None:
            data['msg'] = 'banned_user_id is required'
            return JsonResponse(data)
        #else input is not empty
        #check if banned_user_id is a positive integer
        try:
            banned_user_id = int(banned_user_id)
            if not (banned_user_id) > 0:
                data['msg'] = 'banned_user_id must be a positive integer'
                return JsonResponse(data)
        except:
            data['msg'] = 'banned_user_id must be a positive integer'
            return JsonResponse(data)
        
        try:
            banned_user_obj = login.models.User.objects.get(uid = banned_user_id)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have user with banned_user_id: ' + str(banned_user_id)
            return JsonResponse(data)
        
        try:
            models.User_banned_list.objects.get(user = user_obj, banned_user = banned_user_obj).delete()
        except ObjectDoesNotExist:
            data['msg'] = "user with banned_user_id: " + str(banned_user_id) + ' is not in blacklist'
            return JsonResponse(data)
        else:
            data['success'] = True
            data['msg'] = 'successfully remove user from blacklist'
            return JsonResponse(data)
    else:
        data['msg'] = 'please use GET'
        return JsonResponse(data)


def all_reviews_view(request):
    '''
    get all reviews by giving movie_id.
    the input json has this format:
    {
        "movie_id": "some movie id here, must be a positive integer"
    }
    
    request.method == 'GET'
    '''
    data = {}
    data['success'] = False
    data['msg'] = ''
    data['reviews'] = []
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
            data['msg'] = 'found all reviews for movie_id: ' + str(movie_id)

            movie_detail_dict = movie_detail_to_dict(movie_obj,request,num_review = 1000)
            data['reviews'] = movie_detail_dict['reviews']
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
    
    request.method == 'POST'
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
            # create a new record for the new review in database.
            models.Review.objects.create(user = user_obj, movie = movie_obj, review_comment = review_comment, rating_number = rating_number, date = date)
            # update the average_rating and votecount for the movie.
            update_movie_rating_record(movie_id, float(rating_number), 'new')
        except IntegrityError:
            data['msg'] = 'each user can only leave one review for a movie, but reviews are editable'
            return JsonResponse(data)
        else:
            data['success'] = True
            data['msg'] = 'successfully create a new review'
            return JsonResponse(data)
    else:
        data['msg'] = 'please use POST'
        return JsonResponse(data)


def my_reviews_view(request):
    '''
    get all reviews left by the current user
    input: No input
    
    request.method == 'GET'
    '''
    data = {}
    data['success'] = False
    data['msg'] = ''
    data['reviewlist'] = []
    if request.method == 'GET':
        # Check if the user has already logged in.
        # If user has not logged in, return an error msg to frontend.
        # If user has logged in, let user view his/her reviewlist
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
        
        data['success'] = True
        data['msg'] = 'successfully get reviewlist of the current user'
        review_obj_list = models.Review.objects.filter(user__exact = user_obj).order_by('-date')
        for review_obj in review_obj_list:
            data['reviewlist'].append(review_to_dict(review_obj))
        return JsonResponse(data)
        
    else:
        data['msg'] = 'please use GET'
        return JsonResponse(data)


def get_review_view(request):
    '''
    get a single review left by the current user, for movie_id.
    the input json has this format:
    {
        "movie_id": "some movie id here, must be a positive integer"
    }
    
    request.method == 'GET'
    '''
    data = {}
    data['success'] = False
    data['msg'] = ''
    data['review'] = []
    if request.method == 'GET':
        # Check if the user has already logged in.
        # If user has not logged in, return an error msg to frontend.
        # If user has logged in, let user get review left by him/her, for movie_id
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
        
        try:
            review_obj = models.Review.objects.get(user = user_obj, movie = movie_obj)
        except ObjectDoesNotExist:
            data['msg'] = "the current user didn't leave a review for movie_id: " + str(movie_id)
            return JsonResponse(data)
        else:
            data['success'] = True
            data['msg'] = 'found review for movie_id: ' + str(movie_id) + ' left by the current user'
            data['review'].append(review_to_dict(review_obj))
            return JsonResponse(data)
    else:
        data['msg'] = 'please use GET'
        return JsonResponse(data)


def delete_review_view(request):
    '''
    delete the review that was left by the current user, for movie_id
    the input json has this format:
    {
        "movie_id": "some movie id here, must be a positive integer"
    }
    
    request.method == 'GET'
    '''
    data = {}
    data['success'] = False
    data['msg'] = ''
    if request.method == 'GET':
        # Check if the user has already logged in.
        # If user has not logged in, return an error msg to frontend.
        # If user has logged in, let user delete review left by him/her, for movie_id
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
        
        try:
            # get the rating_number of the review to be deleted
            rating_number = models.Review.objects.get(user=user_obj, movie=movie_obj).rating_number
            models.Review.objects.get(user = user_obj, movie = movie_obj).delete()
            # update the average_rating and votecount for the movie.
            update_movie_rating_record(movie_id, float(rating_number), 'delete')
        except ObjectDoesNotExist:
            data['msg'] = "the current user didn't leave a review for movie_id: " + str(movie_id)
            return JsonResponse(data)
        else:
            data['success'] = True
            data['msg'] = "successfully delete review"
            return JsonResponse(data)
    else:
        data['msg'] = 'please use GET'
        return JsonResponse(data)


def edit_review_view(request):
    '''
    edit the review that was left by the current user, for movie_id
    Note that only review_comment and rating_number are editable
    
    the input json has this format:
    {
        "movie_id": "some movie id here, must be a positive integer",
        "review_comment": "some comment here, must be a string",
        "rating_number": "some rating number here, must be a positive number",
    }
    
    request.method == 'POST'
    '''
    data = {}
    data['success'] = False
    data['msg'] = ''
    if request.method == 'POST':
        # Check if the user has already logged in.
        # If user has not logged in, return an error msg to frontend.
        # If user has logged in, let user edit review
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
        
        # return review_obj, from models.Review database, by giving user_obj, movie_obj
        try:
            review_obj = models.Review.objects.get(user = user_obj, movie = movie_obj)
        except ObjectDoesNotExist:
            data['msg'] = "the current user didn't leave a review for movie_id: " + str(movie_id)
            return JsonResponse(data)
        else:
            # get the previous rating_number
            prev_rating_number = review_obj.rating_number
            # update review_obj
            date = datetime.datetime.now(timezone.utc)
            review_obj.review_comment = review_comment
            review_obj.rating_number = rating_number
            review_obj.date = date
            review_obj.save()
            # update the average_rating and votecount for the movie.
            update_movie_rating_record(movie_id, float(rating_number - prev_rating_number), 'edit')
            # return msg
            data['success'] = True
            data['msg'] = 'successfully edit review'
            return JsonResponse(data)
        
    else:
        data['msg'] = 'please use POST'
        return JsonResponse(data)


def others_wishlist_view(request):
    '''
    get all movies in wishlist of the current user
    input: {
                "username": "a username"
            }

    request.method == 'GET'
    '''
    data = {
        'success': False,
        'msg': '',
        'wishlist': []
    }

    if request.method == 'GET':
        # get the target username
        try:
            req = simplejson.loads(request.body)
            username = req['username'].strip()
        except:
            username = request.GET.get('username')

        # get the target user query from database
        try:
            user_obj = login.models.User.objects.get(name=username)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have user: ' + str(username)
            return JsonResponse(data)

        data['success'] = True
        data['msg'] = 'successfully get wishlist of the target user'

        movie_id_list = list(models.Wish_list.objects.filter(user__exact=user_obj).values_list('movie_id', flat=True))
        useful_keys = {'mid', 'name', 'region', 'released_date', 'average_rating'}
        for mid in movie_id_list:
            movie_obj = models.Movie.objects.get(mid=mid)
            movie_dict = movie_to_dict(movie_obj, request)
            data['wishlist'].append({key: value for key, value in movie_dict.items() if key in useful_keys})
        return JsonResponse(data)

    else:
        data['msg'] = 'please use GET'
        return JsonResponse(data)


def others_reviews_view(request):
    '''
    get all reviews left by the target user
    input: {
                "username" : "a username"
            }

    request.method == 'GET'
    '''
    data = {
        'success': False,
        'msg': '',
        'reviewlist': []
    }
    if request.method == 'GET':
        # get the target username
        try:
            req = simplejson.loads(request.body)
            username = req['username'].strip()
        except:
            username = request.GET.get('username')
        # return user_obj by username from database
        try:
            user_obj = login.models.User.objects.get(name=username)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have user: ' + str(username)
            return JsonResponse(data)

        data['success'] = True
        data['msg'] = 'successfully get reviewlist of the target user'
        review_obj_list = models.Review.objects.filter(user__exact=user_obj).order_by('-date')
        for review_obj in review_obj_list:
            data['reviewlist'].append(review_to_dict(review_obj))
        return JsonResponse(data)

    else:
        data['msg'] = 'please use GET'
        return JsonResponse(data)


def others_page_view(request):
    data = {
        'success': False,
        'msg': [],
        'profile_photo': '',
        'username': '',
        'top_reviews': [],
        'wishlist': []
    }

    if request.method == 'GET':
        # get the target username
        try:
            req = simplejson.loads(request.body)
            username = req['username'].strip()
        except:
            username = request.GET.get('username')

        # check if user is visiting the user's own page
        if request.session.get('login_flag', None):
            session_name = request.session.get('name', None)
            if username == session_name:
                my_page_view(request)

        try:
            user_obj = login.models.User.objects.get(name=username)
        except ObjectDoesNotExist:
            data['msg'] = 'target user does not exist'
            return JsonResponse(data)

        data['success'] = True

        if user_obj.profile_photo:
            data['profile_photo'] = str(user_obj.profile_photo)

        data['username'] = username

        reviews_list = models.Review.objects.filter(user__exact=user_obj).order_by('-date')[:5]
        for review_obj in reviews_list:
            data['top_reviews'].append(review_to_dict(review_obj))

        movie_ids = list(models.User.objects.get(name=username).wish_list_set.values('movie')[:5])
        movie_ids = [e['movie'] for e in movie_ids]
        if movie_ids:
            data['wishlist'] = list(models.Movie.objects.filter(mid__in=movie_ids).values('mid', 'name', 'region', 'released_date','average_rating')[:5])

        return JsonResponse(data)
    else:
        data['msg'] = 'incorrect request method'
        return JsonResponse(data)


def my_page_view(request):
    data = {
        'success': False,
        'msg': [],
        'profile_photo': '',
        'username': '',
        'top_reviews': [],
        'wishlist': []
    }

    if request.method == 'GET':
        # check if user is visiting the user's own page
        if not request.session.get('login_flag', None):
            data['msg'] = 'user did not log in'
            return JsonResponse(data)

        username = request.session.get('name', None)

        try:
            user_obj = login.models.User.objects.get(name=username)
        except ObjectDoesNotExist:
            data['msg'] = 'target user does not exist'
            return JsonResponse(data)

        data['success'] = True

        if user_obj.profile_photo:
            data['profile_photo'] = str(user_obj.profile_photo)

        data['username'] = username

        reviews_list = models.Review.objects.filter(user__exact=user_obj).order_by('-date')[:5]
        for review_obj in reviews_list:
            data['top_reviews'].append(review_to_dict(review_obj))

        movie_ids = list(models.User.objects.get(name=username).wish_list_set.values('movie')[:5])
        movie_ids = [e['movie'] for e in movie_ids]
        if movie_ids:
            data['wishlist'] = list(models.Movie.objects.filter(mid__in=movie_ids).values('mid', 'name', 'region', 'released_date','average_rating')[:5])

        return JsonResponse(data)

    else:
        data['msg'] = 'incorrect request method'
        return JsonResponse(data)

