from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from . import models  # models in movies App
import login.models  # models in login App
from django.db.models import Avg
import simplejson
import datetime
from django.utils import timezone
from django.http import JsonResponse
import pdb
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django_pandas.io import read_frame
import pandas as pd
import numpy as np

''' HELPER FUNCTIONS '''


def get_banned_user_obj_list(user_obj):
    """
    This function returns a list of user objects that were banned by the input user object.
    :param user_obj: A user object
    :return: A list of banned user objects
                [user_obj_1, user_obj_2, ... ]
    e.g.
        User 'pete@123.com' banned user 'holly@123.com' and user '1@1.1'.
        when this function is called, the input user object is:
            user_obj = models.User.objects.get(name = 'pete@123.com')
        It will return:
            [user_obj('holly@123.com'), user_obj('1@1.1')]
    """
    banned_user_obj_list = [user_banned_list_obj.banned_user for user_banned_list_obj in user_obj.banned_user_set.all()]
    return banned_user_obj_list


def movie_to_dict(movie_obj, request):
    """
    This function converts a movie_object to a dictionary, containing
        mid, name, list of genre type, description, region, released_date, director_name,
        poster image path and list of cast names.
    :param movie_obj: A movie object
    :param request: A request from frontend
    :return: A dictionary contains information mentioned above. for example
                {
                    'mid': 1,
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
    """
    movie = {
        'mid': movie_obj.mid,
        'name': movie_obj.name,
        'genre': [movie_genre_obj.genre_type for movie_genre_obj in movie_obj.movie_genre_set.all()],
        'description': movie_obj.description,
        'region': movie_obj.region,
        'released_date': movie_obj.released_date,
        'director': movie_obj.director.name,
        'poster': str(movie_obj.poster),
        'cast': [cast_obj.cast.name for cast_obj in movie_obj.cast_set.all()]
    }

    # if the user has logged in
    if request.session.get('login_flag', None):
        user_name = request.session.get('name', None)
        # return user_obj by user_name from login.models.User database
        try:
            user_obj = login.models.User.objects.get(name=user_name)
        except ObjectDoesNotExist:  # should never goes into this statement
            banned_user_obj_list = []
        else:
            banned_user_obj_list = get_banned_user_obj_list(user_obj)
        finally:
            movie['average_rating'] = models.Review.objects.filter(movie_id__exact=movie['mid']) \
                .exclude(user__in=banned_user_obj_list) \
                .aggregate(Avg('rating_number', distinct=True))['rating_number__avg']

    # else the user does not log in    
    else:
        movie['average_rating'] = models.Review.objects.filter(movie_id__exact=movie['mid']) \
            .aggregate(Avg('rating_number', distinct=True))['rating_number__avg']

    if movie['average_rating'] is not None:
        movie['average_rating'] = round(movie['average_rating'], 1)

    return movie


def review_to_dict(review_obj):
    """
    This function converts a review_obj to a dictionary, containing
        user_id, user_name, movie_id, movie_name, review_comment, rating_number and date.

    :param review_obj: A review object
    :return: A dictionary contains information mentioned above. for example
                {
                    'user_id': 4,
                    'user_name': '4@4.4',
                    'movie_id': 5,
                    'movie_name': 'Avengers: Age of Ultron',
                    'review_comment': "Marvel's The Avengers (2012) is an awesome movie.",
                    'rating_number': 5.0,
                    'date': datetime.datetime(2013, 2, 3, 6, 37, 24, tzinfo=<UTC>)
                }
    """
    review = {
        'user_id': review_obj.user.uid,
        'user_name': review_obj.user.name,
        'movie_id': review_obj.movie.mid,
        'movie_name': review_obj.movie.name,
        'review_comment': review_obj.review_comment,
        'rating_number': review_obj.rating_number,
        'date': review_obj.date
    }
    return review


def movie_detail_to_dict(movie_obj, request, num_review):
    """
    This function converts movie_object to a dictionary, containing
        mid, name, list of genre type, description, region, released_date, director_name,
        poster image path, list of cast name and list of reviews.

    :param movie_obj: A movie object
    :param request: A request from frontend
    :param num_review: An integer indicates total number of reviews
    :return: A dictionary contains information mentioned above. for example
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

    NOTE that if user has logged in, list of reviews will not include reviews from its block list.
    """
    movie_dict = movie_to_dict(movie_obj, request)
    movie_dict['reviews'] = []

    # if the user has logged in
    if request.session.get('login_flag', None):
        user_name = request.session.get('name', None)
        # return user_obj by user_name from login.models.User database
        try:
            user_obj = login.models.User.objects.get(name=user_name)
        except ObjectDoesNotExist:
            review_obj_list = movie_obj.review_set.all()
        else:
            banned_user_obj_list = get_banned_user_obj_list(user_obj)
            review_obj_list = movie_obj.review_set.exclude(user__in=banned_user_obj_list)

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
    """
    This function will update movie's average rating in Movie table when a new review for it has been added.

    :param movie_id: A movie id
    :param rating_number: A decimal rating number with one decimal digit, from 0 to 5
    :param operation: A string be either 'new', 'edit' or 'delete'
    :return: N/A

    This function will conduct different operation on average rating upon operation parameter.
    """
    movie = models.Movie.objects.get(mid=movie_id)
    if operation == 'new':
        # Update the average_rating and votecount for the movie.
        movie.average_rating = (float(movie.average_rating) * float(movie.votecount) + rating_number) / (
                    movie.votecount + 1)
        movie.votecount += 1
        movie.save()
    elif operation == 'delete':
        movie.average_rating = (float(movie.average_rating) * float(movie.votecount) - float(rating_number)) / (
                    movie.votecount - 1)
        movie.votecount -= 1
        movie.save()
    elif operation == 'edit':
        movie.average_rating = float(movie.average_rating) + (float(rating_number) / movie.votecount)
        movie.save()


def similar_movie(movie_title, names_list):
    """
    This functions returns a list of similar movie names upon given movie title and user's review history and wish list.

    :param movie_title: A movie title
    :param names_list: A list of movie names extracted from user's review history and wish list
    :return: A list of movie names, for example
                ['movie1', 'movie2', 'movie3', ... ]

    If names_list is empty, which indicates the user didn't log in or doesn't have any movies in review history and wish list,
        then returned movies are based on movie_title.
    """
    # covert movie features into count vector
    df = read_frame(models.MovieFeatures.objects.all())
    count = CountVectorizer()
    # generate cosine similarity matrix of all movies
    count_matrix = count.fit_transform(df['bag_of_words'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    indices = pd.Series(df['title'])

    # get the most similar 10 movies based on cosine similarity matrix
    def recommend(title, cosine_sim=cosine_sim):
        recommended_movies = []
        idx = indices[indices == title].index[0]
        score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)
        top_10_indices = list(score_series.iloc[1:11].index)
        for i in top_10_indices:
            recommended_movies.append(list(df['title'])[i])
        return recommended_movies

    # check if name_list is empty
    if len(names_list) > 0:
        similar_movies = []
        for name in names_list:
            similar_movies.extend(recommend(name))
        return similar_movies[:10]
    else:
        return recommend(movie_title)


''' APIs '''


def search_view(request):
    """
    This API will search for movies upon input keywords.

    :param request: request contains a Json format data
                        {
                          "search": "some key words here"
                        }

    :return: A Json format data
            {
              "success": true,
              "result": [
                          {
                          "mid": "movie id",
                          "name": "movie name",
                          "released_date": "released year",
                          "poster": "src path of poster",
                          "average_rating": "latest averaged rating"
                        },
                          {
                          "mid": "movie id",
                          "name": "movie name",
                          "released_date": "released year",
                          "poster": "src path of poster",
                          "average_rating": "latest averaged rating"
                        },
                          ...
                      ]
            }

    { "success": true, "result": []} indicates no related movie is found.

    When searching for movies, keywords can be:
        a movie name or a substring of a movie name;
        a director name or a substring of a director name;
        a region or a substring of a region;
        a genre or a substring of a genre;
        Any combination of keywords mentioned above.

    When input keywords are multiple constraints, the search will be conducted based on a conjunction of input keywords.
    For example, if input keywords are UK 2003 quentin, it will search for Quentin Tarantino's movies made in UK in 2003.
    """
    if request.method == 'GET':
        # get data from request
        try:
            req = simplejson.loads(request.body)
            key_words = req['search'].strip()
        except:
            key_words = request.GET.get('search')
        # check if input is empty
        if not key_words:
            data = {
                'success': False,
                'msg': 'empty input'
            }
            return JsonResponse(data)

        # construct returned data
        data = {
            'success': True,
            'result': []
        }

        key_words_list = key_words.split(' ')

        # create empty movie name lists
        by_genre = []
        by_director = []
        by_time = []
        by_region = []

        all_genres = ['action', 'animation', 'comedy', 'crime', 'documentary', 'drama', 'fantacy', 'horror', 'kids',
                      'family', 'mystery', 'romance', 'science', 'fiction']

        # get movies that keyword is or is a substring of movie names
        by_name = list(models.Movie.objects.filter(name__icontains=key_words).values_list('mid', flat=True))

        for word in key_words_list:
            if word:
                # get movies that keyword is or is a substring of genres
                if word.lower() in all_genres:
                    id_list = list(models.Movie_genre.objects.filter(genre_type__icontains=word).values_list('movie_id',
                                                                                                             flat=True).distinct())
                    by_genre.extend(id_list)

                # get movies that keyword is or is a substring of a director's name
                pid_list = list(
                    models.Person.objects.filter(name__icontains=word).values_list('pid', flat=True).distinct())
                if pid_list:
                    id_list = list(
                        models.Movie.objects.filter(director_id__in=pid_list).values_list('mid', flat=True).distinct())
                    by_director.extend(id_list)

                # get movies that keyword is a time
                if re.findall(r'[1-2][0-9][0-9][0-9]', word):
                    id_list = list(
                        models.Movie.objects.filter(released_date__year=word).values_list('mid', flat=True).distinct())
                    by_time.extend(id_list)

                # get movies that keyword is a region
                id_list = list(models.Movie.objects.filter(region__icontains=word).values_list('mid', flat=True))
                by_region.extend(id_list)

        # merge search results
        if by_name:
            result_id_list = by_name + by_genre + by_director + by_time + by_region
        else:
            if not by_genre and not by_director and not by_region and not by_time:
                return JsonResponse(data)

            set_list = [set(by_genre), set(by_director), set(by_time), set(by_region)]
            set_list = [s for s in set_list if len(s) != 0]
            result_id_list = set.intersection(*set_list)

        # get all information needed
        movie_list = list(
            models.Movie.objects.filter(mid__in=result_id_list).values('mid', 'name', 'released_date', 'poster',
                                                                       'average_rating'))

        # sort results based on ratings.
        # if two are the same then sort results alphabetically.
        if movie_list:
            data['result'] = sorted(list(movie_list), key=lambda x: (-x['average_rating'], x['name']))

        return JsonResponse(data)

    return


def movie_list_view(request):
    """
    This API will return all movies detail by calling 'movie_to_dict' function for all movie objects in database
    and return in Json form.

    :param request: A request from frontend, the method of which should be GET
    :return: A Json format data
                {
                "success": true,
                "movies":[
                            {
                              "mid": 1,
                              "name": "test_movie1",
                              "genre":[
                                "test_genre1",
                                "test_genre12",
                                "test_genre3"
                              ],
                              "description": "test_movie1_description",
                              "region": "US",
                              "released_date": "2020-10-30T09:37:52Z",
                              "director": "test_director1",
                              "poster": "../movies/posters/壁纸.jpg",
                              "cast":[
                                "test_actor1",
                                "test_actor2"
                              ],
                              "average_rating":4.5
                            },

                            {
                              "mid": 2,
                              "name": "test_movie2",
                              "genre":["test_genre1", "test_genre3"],
                              "description": "test_movie2 description",
                              "region": "SYD",
                              "released_date": "2020-10-05T00:00:00Z",
                              "director": "test_director2",
                              "poster": "../movies/posters/终将成为你6.jpg",
                              "cast":["test_actor1"],
                              "average_rating":4.3
                            },

                            ...

                            {
                              ...
                            },

                          ]
                }
    "success" indicates http://127.0.0.1:8000/movies/ successfully return all movies.
    NOTE that if the user is logged in, the "average_rating" field will exclude reviews given by users in banned list.
    """
    data = {'success': False, 'movies': []}
    if request.method == 'GET':
        data['success'] = True
        # get information of all movie objects
        movie_obj_list = models.Movie.objects.order_by('name')[:]
        for movie_obj in movie_obj_list:
            data['movies'].append(movie_to_dict(movie_obj, request))
    return JsonResponse(data)


def detail_view(request):
    """
    This API gets a movie detail by a giving movie_id, along with recommended movies.
    If the user has logged in, the similar movies will be found based on the user's review history and wish list.
    Otherwise, movies similar to the movie of given movie_id will be returned.

    :param request: request contains a Json format data
                    {
                      "movie_id": "some movie id here, must be a positive integer"
                    }
    :return: A Json format data
            {
              "success": true/false,
              "msg": "some message here"
              "movies": [
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
              ]
              "similar_movies": [
                          {
                          "mid": "movie id",
                          "name": "movie name",
                          "released_date": "released year",
                          "poster": "src path of poster",
                          "average_rating": "latest averaged rating"
                        },
                          {
                          "mid": 5,
                          "name": "Avengers: Age of Ultron",
                          "released_date": "2015-05-01T00:00:00Z",
                          "poster": "src path of poster",
                          "average_rating": 3.0
                        },
                          ...
                      ]
            }

    {"success": false, "msg": "movie_id is required", "movie": []} indicates there is no input in the GET Query Parameters.
    {"success": false, "msg": "movie_id must be a positive integer", "movie": []} indicates the input is not a positive integer.
    {"success": false, "msg": "does not have movie with movie_id: " + str(movie_id), "movie": []} indicates there is no movie with mid == movie_id
    {"success": true, "msg": "found movie with movie_id: " + str(movie_id), "movie": [{...}]} indicates there is a movie with mid == movie_id

    NOTE that if the user is logged in, the "reviews" field will exclude reviews given by users in banned list.
    """
    data = {'success': False, 'msg': '', 'movie': []}
    if request.method == 'GET':
        # get data from request
        try:
            req = simplejson.loads(request.body)
            movie_id = req['movie_id'].strip()
        except:
            movie_id = request.GET.get('movie_id')

        # check if input is empty
        if movie_id is None:
            data['msg'] = 'movie_id is required'
            return JsonResponse(data)

        # check if movie_id is valid
        try:
            movie_id = int(movie_id)
            if not (movie_id > 0):
                data['msg'] = 'movie_id must be a positive integer'
                return JsonResponse(data)
        except:
            data['msg'] = 'movie_id must be a positive integer'
            return JsonResponse(data)

        # get needed information for the given movie
        try:
            movie_obj = models.Movie.objects.get(mid=movie_id)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have movie with movie_id: ' + str(movie_id)
            return JsonResponse(data)
        else:
            data['success'] = True
            data['msg'] = 'found movie with movie_id: ' + str(movie_id)
            data['movie'].append(movie_detail_to_dict(movie_obj, request, num_review=5))

            # check if user has logged in
            if request.session.get('login_flag', None):
                try:
                    username = request.session['name']
                    uid = login.models.User.objects.get(name=username).uid
                except:
                    similar_list = similar_movie(movie_obj.name, [])

                # get movies from the user's review history and wish list
                review_ids = list(models.Review.objects.filter(user_id=uid).values_list('movie_id', flat=True))
                review_names = list(models.Movie.objects.filter(mid__in=review_ids).values_list('name', flat=True))
                wishlist_ids = list(models.Wish_list.objects.filter(user_id=uid).values_list('movie_id', flat=True))
                wishlist_names = list(models.Movie.objects.filter(mid__in=wishlist_ids).values_list('name', flat=True))
                names_list = np.random.choice(np.concatenate([review_names, wishlist_names]),
                                              len(review_names) + len(wishlist_names), replace=False)
            else:
                names_list = []

            # get a list of similar movie names
            similar_list = similar_movie(movie_obj.name, names_list)
            data['similar_movies'] = list(
                models.Movie.objects.filter(name__in=similar_list).values('mid', 'name', 'released_date', 'poster',
                                                                          'average_rating'))
            return JsonResponse(data)

    else:
        data['msg'] = "please use GET"
        return JsonResponse(data)


def add_to_wishlist_view(request):
    """
    This API adds movie given by movie_id to user's wish_list.

    :param request: request contains a Json format data
                        {
                            "movie_id": "some movie id here, must be a positive integer"
                        }
    :return: A Json format data
                {
                  "success": true/false,
                  "msg": "some message here"
                }

    {"success": false, "msg": "user does not log in"} indicates that user does not log in.
    {"success": false, "msg": "movie_id is required"} means the input json dose not have movie_id field.
    {"success": false, "msg": "movie_id must be a positive integer"} indicates the input json does not follow the above input request.
    {"success": false, "msg": "does not have movie with movie_id: " + str(movie_id)} indicates
        the given movie_id field does not match any record in Movie database
    {"success": false, "msg": "movie already in wishlist"} indicates t
        he given movie is already in wishlist
    {"success": true, "msg": "successfully insert movie to wishlist"} indicates
        the given movie is successfully inserted into wishlist
    """
    data = {'success': False, 'msg': ''}
    if request.method == 'GET':
        # check if the user has already logged in
        # if user has not logged in, return an error msg to frontend
        # if user has logged in, let user add movie to his/her wishlist
        if not request.session.get('login_flag', None):
            data['msg'] = 'user does not log in'
            return JsonResponse(data)
        # else use is logged in
        user_name = request.session.get('name', None)
        # return user_obj by user_name from login.models.User database
        try:
            user_obj = login.models.User.objects.get(name=user_name)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have user: ' + str(user_name)
            return JsonResponse(data)

        try:
            req = simplejson.loads(request.body)
            movie_id = req['movie_id'].strip()
        except:
            movie_id = request.GET.get('movie_id')
        # check if input is empty
        if movie_id == None:
            data['msg'] = 'movie_id is required'
            return JsonResponse(data)
        # else input is not empty

        # check if movie_id is a positive integer
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

        try:
            models.Wish_list.objects.create(user=user_obj, movie=movie_obj)
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
    """
    This API gets all movies in wishlist of the current user.

    :param request: A request from frontend, the method of which should be GET
    :return: A Json format data
                {
                  "success": true,
                  "msg": "successfully get wishlist of the current user",
                  "wishlist":[
                                  {
                                    "mid": 4,
                                    "name": "The Avengers",
                                    "region": "United States",
                                    "released_date": "2012-05-04T12:00:00Z",
                                    "average_rating": 3.8,
                                    "poster": "..."
                                  },
                                  {
                                    "mid": 5,
                                    "name": "Avengers: Age of Ultron",
                                    "region": "United States",
                                    "released_date": "2015-05-01T00:00:00Z",
                                    "average_rating": 3.0,
                                    "poster": "..."
                                  }
                                ]
                }

    {"success": false, "msg": "user does not log in", "wishlist":[]} indicates that user does not log in.
    {"success": true, "msg": "successfully get wishlist of the current user", "wishlist":[...]} means
        successfully get wishlist of the current user.
    """
    data = {'success': False, 'msg': '', 'wishlist': []}
    if request.method == 'GET':
        # check if the user has already logged in.
        # if user has not logged in, return an error msg to frontend.
        # if user has logged in, let user view his/her wishlist
        if not request.session.get('login_flag', None):
            data['msg'] = 'user does not log in'
            return JsonResponse(data)
        # else use is logged in
        user_name = request.session.get('name', None)
        # return user_obj by user_name from login.models.User database
        try:
            user_obj = login.models.User.objects.get(name=user_name)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have user: ' + str(user_name)
            return JsonResponse(data)

        data['success'] = True
        data['msg'] = 'successfully get wishlist of the current user'

        movie_id_list = list(
            models.Wish_list.objects.filter(user__exact=user_obj).order_by('movie').values_list('movie_id', flat=True))
        useful_keys = {'mid', 'name', 'region', 'released_date', 'average_rating', 'poster'}
        for mid in movie_id_list:
            movie_obj = models.Movie.objects.get(mid=mid)
            movie_dict = movie_to_dict(movie_obj, request)
            data['wishlist'].append({key: value for key, value in movie_dict.items() if key in useful_keys})

        return JsonResponse(data)

    else:
        data['msg'] = 'please use GET'
        return JsonResponse(data)


def remove_from_wishlist_view(request):
    """
    This API removes movie given by movie_id from user's wish_list.

    :param request: request contains a Json format data
                        {
                            "movie_id": "some movie id here, must be a positive integer"
                        }
    :return: A Json format data
                {
                  "success": true/false,
                  "msg": "some message here"
                }

    {"success": false, "msg": "user does not log in"} indicates that user does not log in.
    {"success": false, "msg": "movie_id is required"} means the input json dose not have movie_id field.
    {"success": false, "msg": "movie_id must be a positive integer"} indicates the input json does not follow the above input request.
    {"success": false, "msg": "does not have movie with movie_id: " + str(movie_id)} indicates
        the given movie_id field does not match any record in Movie database.
    {"success": false, "msg": "movie with movie_id: " + str(movie_id) + " is not in wishlist"} indicates
        the given movie is not in the user's wishlist.
    {"success": true, "msg": "successfully remove movie from wishlist"} indicates
        the given movie is successfully removed from the user's wishlist.
    """
    data = {'success': False, 'msg': ''}
    if request.method == 'GET':
        # check if the user has already logged in.
        # if user has not logged in, return an error msg to frontend.
        # if user has logged in, let user remove movie from his/her wishlist
        if not request.session.get('login_flag', None):
            data['msg'] = 'user does not log in'
            return JsonResponse(data)
        # else use is logged in
        user_name = request.session.get('name', None)
        # return user_obj by user_name from login.models.User database
        try:
            user_obj = login.models.User.objects.get(name=user_name)
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
        # else input is not empty

        # check if movie_id is a positive integer
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

        try:
            models.Wish_list.objects.get(user=user_obj, movie=movie_obj).delete()
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
    """
    This API adds user, that the current user doesn't like given by banned_user_id, to the current user's blacklist.

    :param request: request contains a Json format data
    :return: A Json format data
                {
                  "success": true/false
                  "msg": "some message here",
                }

    {"success": false, "msg": "user does not log in"} indicates that user does not log in.
    {"success": false, "msg": "banned_user_id is required"} means the input json dose not have banned_user_id field.
    {"success": false, "msg": "banned_user_id must be a positive integer"} indicates
        the input json does not follow the above input request.
    {"success": false, "msg": "does not have user with banned_user_id: " + str(banned_user_id)} indicates that
        the user you want to add to your blacklist does not exist.
    {"success": false, "msg": "user cannot add itself to its blacklist"} indicates that
        user cannot add itself to its blacklist.
    {"success": false, "msg": "banned_user_id: " + str(banned_user_id) + " already in blacklist"} indicates that
        the user you want to block is already in your blacklist.
    {"success": true, "msg": "successfully insert banned_user_id: " + str(banned_user_id) + " into blacklist"} indicates
        that now the user with banned_user_id is in your blacklist.
    """
    data = {'success': False, 'msg': ''}
    if request.method == 'GET':
        # Check if the current user has already logged in.
        # If user has not logged in, return an error msg to frontend.
        # If user has logged in, let user add banned user he/she doesn't like, to his/her blacklist
        if not request.session.get('login_flag', None):
            data['msg'] = 'user does not log in'
            return JsonResponse(data)
        # else current use is logged in
        curr_user_name = request.session.get('name', None)
        # return curr_user_obj by curr_user_name from login.models.User database
        try:
            curr_user_obj = login.models.User.objects.get(name=curr_user_name)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have user: ' + str(curr_user_name)
            return JsonResponse(data)

        try:
            req = simplejson.loads(request.body)
            banned_user_id = req['banned_user_id'].strip()
        except:
            banned_user_id = request.GET.get('banned_user_id')
        # check if input is empty
        if banned_user_id is None:
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
            banned_user_obj = login.models.User.objects.get(uid=banned_user_id)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have user with banned_user_id: ' + str(banned_user_id)
            return JsonResponse(data)

        if curr_user_obj.uid == banned_user_obj.uid:
            data['msg'] = 'user cannot add itself to its blacklist'
            return JsonResponse(data)

        try:
            models.User_banned_list.objects.create(user=curr_user_obj, banned_user=banned_user_obj)
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
    """
    This API gets all users in bannedlist of the current user.

    :param request: A request from frontend, the method of which should be GET
    :return: A Json format data
                {
                  "success": true,
                  "msg": "successfully get blacklist of the current user",
                  "bannedlist":[
                                  {
                                    "uid": 2,
                                    "name": "holly@123.com"
                                  },
                                  {
                                    "uid": 6,
                                    "name": "6@6.6"
                                  },
                                  {
                                    "uid": 7,
                                    "name": "7@7.7"
                                  }
                                ]
                }

    {"success": false, "msg": "user does not log in", "bannedlist":[]} indicates that user does not log in.
    {"success": true, "msg": "successfully get blacklist of the current user", "bannedlist":[...]} indicates
        that successfully get blacklist of the current user.
    """
    data = {'success': False, 'msg': '', 'bannedlist': []}
    if request.method == 'GET':
        # check if the user has already logged in.
        # if user has not logged in, return an error msg to frontend.
        # if user has logged in, let user view his/her blacklist
        if not request.session.get('login_flag', None):
            data['msg'] = 'user does not log in'
            return JsonResponse(data)
        # else use is logged in
        user_name = request.session.get('name', None)
        # return user_obj by user_name from login.models.User database
        try:
            user_obj = login.models.User.objects.get(name=user_name)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have user: ' + str(user_name)
            return JsonResponse(data)

        data['success'] = True
        data['msg'] = 'successfully get blacklist of the current user'

        banned_user_obj_list = get_banned_user_obj_list(user_obj)
        data['bannedlist'] = [{"uid":banned_user_obj.uid, "name":banned_user_obj.name, "profile_photo":str(banned_user_obj.profile_photo)} for banned_user_obj in banned_user_obj_list]
        return JsonResponse(data)

    else:
        data['msg'] = 'please use GET'
        return JsonResponse(data)


def remove_from_bannedlist_view(request):
    """
    This API removes banned_user given by banned_user_id from user's blacklist.

    :param request: request contains a Json format data
                        {
                          "banned_user_id": "some banned_user_id, that you want to no longer block, must be a positive integer"
                        }
    :return: A Json format data
                {
                  "success": true/false,
                  "msg": "some message here"
                }

    {"success": false, "msg": "user does not log in"} indicates that user does not log in.
    {"success": false, "msg": "banned_user_id is required"} means the input json dose not have banned_user_id field.
    {"success": false, "msg": "banned_user_id must be a positive integer"} indicates
        the input json does not follow the above input request.
    {"success": false, "msg": "does not have user with banned_user_id: " + str(banned_user_id)} indicates
        the given banned_user_id field does not match any record in User database.
    {"success": false, "msg": "user with banned_user_id: " + str(banned_user_id) + " is not in blacklist"} indicates
        the given banned_user is not in the current user's blacklist.
    {"success": true, "msg": "successfully remove user from blacklist"} indicates
        the given banned_user is successfully removed from the current user's blacklist.
    """
    data = {'success': False, 'msg': ''}
    if request.method == 'GET':
        # check if the user has already logged in.
        # if user has not logged in, return an error msg to frontend.
        # if user has logged in, let user remove banned_user from his/her blacklist
        if not request.session.get('login_flag', None):
            data['msg'] = 'user does not log in'
            return JsonResponse(data)
        # else use is logged in
        user_name = request.session.get('name', None)
        # return user_obj by user_name from login.models.User database
        try:
            user_obj = login.models.User.objects.get(name=user_name)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have user: ' + str(user_name)
            return JsonResponse(data)

        try:
            req = simplejson.loads(request.body)
            banned_user_id = req['banned_user_id'].strip()
        except:
            banned_user_id = request.GET.get('banned_user_id')
        # check if input is empty
        if banned_user_id is None:
            data['msg'] = 'banned_user_id is required'
            return JsonResponse(data)
        # else input is not empty
        # check if banned_user_id is a positive integer
        try:
            banned_user_id = int(banned_user_id)
            if not (banned_user_id) > 0:
                data['msg'] = 'banned_user_id must be a positive integer'
                return JsonResponse(data)
        except:
            data['msg'] = 'banned_user_id must be a positive integer'
            return JsonResponse(data)

        try:
            banned_user_obj = login.models.User.objects.get(uid=banned_user_id)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have user with banned_user_id: ' + str(banned_user_id)
            return JsonResponse(data)

        try:
            models.User_banned_list.objects.get(user=user_obj, banned_user=banned_user_obj).delete()
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
    """
    This API gets all reviews by giving movie_id.

    :param request: request contains a Json format data
                    {
                        "movie_id": "some movie id here, must be a positive integer"
                    }

    :return: A Json format data
                {
                  "success": true/false,
                  "msg": "some message here"
                  "reviews":[
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

    "success" indicates whether successfully return all reviews.

    "msg" shows the current state.

    {"success": false, "msg": "movie_id is required", "reviews": []} indicates there is no input in the GET Query Parameters.
    {"success": false, "msg": "movie_id must be a positive integer", "reviews": []} indicates
        the input is not a positive integer.
    {"success": false, "msg": "does not have movie with movie_id: " + str(movie_id), "reviews": []} indicates
        there is no movie with mid == movie_id
    {"success": true, "msg": "found all reviews for movie_id: " + str(movie_id), "reviews": [{...}, {...}]} indicates
        there is a movie with mid == movie_id, and found all reviews for this movie.

    NOTE that if the user is logged in, the "reviews" field will exclude reviews given by users in banned list.
    """
    data = {'success': False, 'msg': '', 'reviews': []}
    if request.method == 'GET':
        try:
            req = simplejson.loads(request.body)
            movie_id = req['movie_id'].strip()
        except:
            movie_id = request.GET.get('movie_id')
        # check if input is empty
        if movie_id == None:
            data['msg'] = 'movie_id is required'
            return JsonResponse(data)
        # else input is not empty

        # check if movie_id is a positive integer
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
            data['msg'] = 'found all reviews for movie_id: ' + str(movie_id)

            movie_detail_dict = movie_detail_to_dict(movie_obj, request, num_review=1000)
            data['reviews'] = movie_detail_dict['reviews']
            return JsonResponse(data)

    else:
        data['msg'] = "please use GET"
        return JsonResponse(data)


def new_review_view(request):
    """
    This API will creates a new Review tuple upon request.

    :param request: request contains a Json format data
                        {
                            "movie_id": "some movie id here, must be a positive integer",
                            "review_comment": "some comment here, must be a string",
                            "rating_number": "some rating number here, must be a positive number",
                        }

    :return: A Json format data
                {
                  "success": true/false
                  "msg": "some message here",
                }

    "success" indicates whether successfully create new review.
    "msg" shows the current state.

    {"success": false, "msg": "user does not log in"} indicates that user does not log in.
    {"success": false, "msg": "movie_id, review_comment, rating_number are required"} means
        the input json dose not have either movie_id field, or review_comment field, or rating_number field.
    {   "success": false,
        "msg": "movie_id must be a positive integer, review_comment must be a string,
                    rating_number must be a positive number"
        } indicates the input json does not follow the above input request
    {   "success": false,
        "msg": "does not have movie with movie_id: " + str(movie_id)
        } indicates the given movie_id field does not match any record in Movie database
    {"success": false, "msg": "each user can only leave one review for a movie, but reviews are editable"} indicates
        that there is already a review for the current user and the given movie
    {"success": true, "msg": "successfully create a new review"} indicates a new review is created
    """
    data = {'success': False, 'msg': ''}
    if request.method == 'POST':
        # check if the user has already logged in.
        # if user has not logged in, return an error msg to frontend.
        # if user has logged in, let user create a new review
        if not request.session.get('login_flag', None):
            data['msg'] = 'user does not log in'
            return JsonResponse(data)
        # else use is logged in
        user_name = request.session.get('name', None)
        # return user_obj by user_name from login.models.User database
        try:
            user_obj = login.models.User.objects.get(name=user_name)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have user: ' + str(user_name)
            return JsonResponse(data)

        req = simplejson.loads(request.body)
        movie_id = req.get('movie_id', None)
        review_comment = req.get('review_comment', None)
        rating_number = req.get('rating_number', None)

        # check if either movie_id, review_comment, rating_number, is empty
        if movie_id is None or review_comment is None or rating_number is None:
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
            movie_obj = models.Movie.objects.get(mid=movie_id)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have movie with movie_id: ' + str(movie_id)
            return JsonResponse(data)

        date = datetime.datetime.now(timezone.utc)

        try:
            # create a new record for the new review in database.
            models.Review.objects.create(user=user_obj, movie=movie_obj, review_comment=review_comment,
                                         rating_number=rating_number, date=date)
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
    """
    This API gets all reviews left by the current user.

    :param request: A request from frontend, the method of which should be GET
    :return: A Json format data
                {
                  "success": true,
                  "msg": "successfully get reviewlist of the current user",
                  "reviewlist":[
                                  {
                                    "user_id": 1,
                                    "user_name": "pete@123.com",
                                    "movie_id": 5,
                                    "movie_name": "Avengers: Age of Ultron",
                                    "review_comment": "some comment here, must be a string",
                                    "rating_number": 1.0,
                                    "date": "2020-11-05T10:20:09.849Z"
                                  },
                                  {
                                    "user_id": 1,
                                    "user_name": "pete@123.com",
                                    "movie_id": 4,
                                    "movie_name": "The Avengers",
                                    "review_comment": "bad movie for movie_id = 4",
                                    "rating_number": 1.0,
                                    "date": "2020-11-05T08:13:28.537Z"
                                  }
                                ]
                }

    {"success": false, "msg": "user does not log in", "reviewlist":[]} indicates that user does not log in.
    {"success": true, "msg": "successfully get reviewlist of the current user", "reviewlist":[...]} indicates
        that successfully get reviewlist of the current user.
    """
    data = {'success': False, 'msg': '', 'reviewlist': []}
    if request.method == 'GET':
        # check if the user has already logged in.
        # if user has not logged in, return an error msg to frontend.
        # if user has logged in, let user view his/her reviewlist
        if not request.session.get('login_flag', None):
            data['msg'] = 'user does not log in'
            return JsonResponse(data)
        # else use is logged in
        user_name = request.session.get('name', None)
        # return user_obj by user_name from login.models.User database
        try:
            user_obj = login.models.User.objects.get(name=user_name)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have user: ' + str(user_name)
            return JsonResponse(data)

        data['success'] = True
        data['msg'] = 'successfully get reviewlist of the current user'
        review_obj_list = models.Review.objects.filter(user__exact=user_obj).order_by('-date')
        for review_obj in review_obj_list:
            data['reviewlist'].append(review_to_dict(review_obj))
        return JsonResponse(data)

    else:
        data['msg'] = 'please use GET'
        return JsonResponse(data)


def get_review_view(request):
    """
    This API gets a single review left by the current user, for movie_id.

    :param request: request contains a Json format data
                        {
                            "movie_id": "some movie id here, must be a positive integer"
                        }
    :return: A Json format data
                {
                  "success": true,
                  "msg": "found review for movie_id: 5 left by the current user",
                  "review":[
                              {
                                "user_id": 1,
                                "user_name": "pete@123.com",
                                "movie_id": 5,
                                "movie_name": "Avengers: Age of Ultron",
                                "review_comment": "some comment here, must be a string",
                                "rating_number": 1.0,
                                "date": "2020-11-05T10:20:09.849Z"
                              }
                            ]
                }

    {"success": false, "msg": "user does not log in", "review": []} indicates user does not log in.
    {"success": false, "msg": "movie_id is required", "review": []} indicates
        the input json dose not have movie_id field.
    {"success": false, "msg": "movie_id must be a positive integer", "review": []} indicates
        the input json does not follow the above input request.
    {"success": false, "msg": "does not have movie with movie_id: " + str(movie_id), "review": []} indicates
        the given movie_id field does not match any record in Movie database.
    {"success": false, "msg": "the current user didn't leave a review for movie_id: " + str(movie_id), "review": []}
        indicates there is no review left by the current user, for movie_id.
    {   "success": true,
        "msg": "found review for movie_id: " + str(movie_id) + " left by the current user", "review": [{...}]
        } indicates found review that was left by the current user, for movie_id.
    """
    data = {'success': False, 'msg': '', 'review': []}
    if request.method == 'GET':
        # check if the user has already logged in.
        # if user has not logged in, return an error msg to frontend.
        # if user has logged in, let user get review left by him/her, for movie_id
        if not request.session.get('login_flag', None):
            data['msg'] = 'user does not log in'
            return JsonResponse(data)
        # else use is logged in
        user_name = request.session.get('name', None)
        # return user_obj by user_name from login.models.User database
        try:
            user_obj = login.models.User.objects.get(name=user_name)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have user: ' + str(user_name)
            return JsonResponse(data)

        try:
            req = simplejson.loads(request.body)
            movie_id = req['movie_id'].strip()
        except:
            movie_id = request.GET.get('movie_id')
        # Check if input is empty
        if movie_id is None:
            data['msg'] = 'movie_id is required'
            return JsonResponse(data)
        # else input is not empty

        # check if movie_id is a positive integer
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

        try:
            review_obj = models.Review.objects.get(user=user_obj, movie=movie_obj)
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
    """
    This API deletes the review that was left by the current user, for movie_id.

    :param request: request contains a Json format data
                        {
                            "movie_id": "some movie id here, must be a positive integer"
                        }

    :return: A Json format data
                {
                  "success": true/false,
                  "msg": "some message here"
                }

    {"success": false, "msg": "user does not log in"} indicates user does not log in.
    {"success": false, "msg": "movie_id is required"} indicates the input json dose not have movie_id field.
    {"success": false, "msg": "movie_id must be a positive integer"} indicates
        the input json does not follow the above input request.
    {"success": false, "msg": "does not have movie with movie_id: " + str(movie_id)} indicates
        the given movie_id field does not match any record in Movie database.
    {"success": false, "msg": "the current user didn't leave a review for movie_id: " + str(movie_id)} indicates
        there is no review left by the current user, for movie_id.
    {"success": true, "msg": "successfully delete review"} indicates
        successfully delete the review left by the current user, for movie_id.
    """
    data = {'success': False, 'msg': ''}
    if request.method == 'GET':
        # check if the user has already logged in.
        # if user has not logged in, return an error msg to frontend.
        # if user has logged in, let user delete review left by him/her, for movie_id
        if not request.session.get('login_flag', None):
            data['msg'] = 'user does not log in'
            return JsonResponse(data)
        # else use is logged in
        user_name = request.session.get('name', None)
        # return user_obj by user_name from login.models.User database
        try:
            user_obj = login.models.User.objects.get(name=user_name)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have user: ' + str(user_name)
            return JsonResponse(data)

        try:
            req = simplejson.loads(request.body)
            movie_id = req['movie_id'].strip()
        except:
            movie_id = request.GET.get('movie_id')
        # check if input is empty
        if movie_id == None:
            data['msg'] = 'movie_id is required'
            return JsonResponse(data)
        # else input is not empty

        # check if movie_id is a positive integer
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

        try:
            # get the rating_number of the review to be deleted
            rating_number = models.Review.objects.get(user=user_obj, movie=movie_obj).rating_number
            models.Review.objects.get(user=user_obj, movie=movie_obj).delete()
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
    """
    This API edits the review that was left by the current user, for movie_id.

    :param request: request contains a Json format data
                        {
                            "movie_id": "some movie id here, must be a positive integer",
                            "review_comment": "some comment here, must be a string",
                            "rating_number": "some rating number here, must be a positive number",
                        }
    :return: A Json format data
                {
                  "success": true/false
                  "msg": "some message here",
                }

    {"success": false, "msg": "user does not log in"} indicates that user does not log in.
    {"success": false, "msg": "movie_id, review_comment, rating_number are required"} means
        the input json dose not have either movie_id field, or review_comment field, or rating_number field.
    {   "success": false,
        "msg": "movie_id must be a positive integer, review_comment must be a string,
            rating_number must be a positive number"} indicates the input json does not follow the above input request.
    {"success": false, "msg": "does not have movie with movie_id: " + str(movie_id)} indicates
        the given movie_id field does not match any record in Movie database.
    {"success": false, "msg": "the current user didn't leave a review for movie_id: " + str(movie_id)} indicates
        there is no review left by the current user, for movie_id.
    {"success": true, "msg": "successfully edit review"} indicates
        successfully edit the review left by the current user, for movie_id.
    """
    data = {'success': False, 'msg': ''}
    if request.method == 'POST':
        # check if the user has already logged in.
        # if user has not logged in, return an error msg to frontend.
        # if user has logged in, let user edit review
        if not request.session.get('login_flag', None):
            data['msg'] = 'user does not log in'
            return JsonResponse(data)
        # else use is logged in
        user_name = request.session.get('name', None)
        # return user_obj by user_name from login.models.User database
        try:
            user_obj = login.models.User.objects.get(name=user_name)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have user: ' + str(user_name)
            return JsonResponse(data)

        req = simplejson.loads(request.body)
        movie_id = req.get('movie_id', None)
        review_comment = req.get('review_comment', None)
        rating_number = req.get('rating_number', None)

        # check if either movie_id, review_comment, rating_number, is empty
        if movie_id is None or review_comment is None or rating_number is None:
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
            movie_obj = models.Movie.objects.get(mid=movie_id)
        except ObjectDoesNotExist:
            data['msg'] = 'does not have movie with movie_id: ' + str(movie_id)
            return JsonResponse(data)

        # return review_obj, from models.Review database, by giving user_obj, movie_obj
        try:
            review_obj = models.Review.objects.get(user=user_obj, movie=movie_obj)
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
    """
    This API gets all movies in wishlist of the current user.

    :param request: request contains a Json format data
                        {
                            "username": "a username"
                        }
    :return: A Json format data
                {
                  "success": true,
                  "msg": "successfully get wishlist of the target user",
                  "wishlist":[
                                  {
                                    "mid": 4,
                                    "name": "The Avengers",
                                    "region": "United States",
                                    "released_date": "2012-05-04T12:00:00Z",
                                    "average_rating": 3.8
                                  },
                                  {
                                    "mid": 5,
                                    "name": "Avengers: Age of Ultron",
                                    "region": "United States",
                                    "released_date": "2015-05-01T00:00:00Z",
                                    "average_rating": 3.0
                                  },
                                  ...
                                ]
                }

    {"success": true, "msg": "successfully get wishlist of the current user", "wishlist":[...]} indicates
        successfully get wishlist of the target user.
    {"success": false, "msg": "does not have user [username]", "wishlist":[]} indicates
        there's something with the target username.
    """
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
        useful_keys = {'mid', 'name', 'region', 'released_date', 'average_rating','poster'}
        for mid in movie_id_list:
            movie_obj = models.Movie.objects.get(mid=mid)
            movie_dict = movie_to_dict(movie_obj, request)
            data['wishlist'].append({key: value for key, value in movie_dict.items() if key in useful_keys})
        return JsonResponse(data)

    else:
        data['msg'] = 'please use GET'
        return JsonResponse(data)


def others_reviews_view(request):
    """
    This API gets all reviews left by the target user.

    :param request: request contains a Json format data
                        {
                            "username" : "a username"
                        }
    :return: A Json format data
                {
                  "success": true,
                  "msg": "successfully get reviewlist of the current user",
                  "reviewlist":[
                                  {
                                    "user_id": 1,
                                    "user_name": "pete@123.com",
                                    "movie_id": 5,
                                    "movie_name": "Avengers: Age of Ultron",
                                    "review_comment": "some comment here, must be a string",
                                    "rating_number": 1.0,
                                    "date": "2020-11-05T10:20:09.849Z"
                                  },
                                  {
                                    "user_id": 1,
                                    "user_name": "pete@123.com",
                                    "movie_id": 4,
                                    "movie_name": "The Avengers",
                                    "review_comment": "bad movie for movie_id = 4",
                                    "rating_number": 1.0,
                                    "date": "2020-11-05T08:13:28.537Z"
                                  },
                                  ...
                                ]
                }

    {"success": true, "msg": "successfully get reviewlist of the target user", "reviewlist":[...]} indicates
        that successfully get reviewlist of the current user.
    {"success": false, "msg": "does not have user [username]", "wishlist":[]} indicates
        there's something with the target username.

    NOTE that once successfully fetch the review list from database,
        all reviews will be sorted by their created/last edited dates, from the latest to the earlist.
    """
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
    """
    This API returns information of requested user.

    :param request: request contains a Json format data
                        {
                          "username": "a user name"
                        }
    :return: A Json format data
                {
                  "success": true,
                  "msg": "",
                  "profile_photo": "a src path of target user's profile photo",
                  "username" : "target user's username",
                  "top_reviews":[
                                  {
                                    "user_id": a user id,
                                    "user_name": "a username",
                                    "movie_id": a movie id,
                                    "movie_name": "the name of the movie",
                                    "review_comment": "some comment here, must be a string",
                                    "rating_number": a rating number from 0 to 5, with one decimal digit,
                                    "date": "the date of review created/last edited"
                                  },
                                  {
                                    "id": 1,
                                    "user_id": 4,
                                    "movie_id": 4,
                                    "movie_name": "The Avengers",
                                    "review_comment": "bad movie for movie_id = 4",
                                    "rating_number": 1.0,
                                    "date": "2020-11-05T08:13:28.537Z"
                                  },
                                  ...
                                ],
                  "wishlist": [
                                {
                                    "mid": a movie id,
                                    "name": "name fo the movie",
                                    "region": "movie's region",
                                    "released_date": "date the movie released",
                                    "average_rating": a rating number from 0 to 5, with one decimal digit
                                  },
                                  {
                                    "mid": 5,
                                    "name": "Avengers: Age of Ultron",
                                    "region": "United States",
                                    "released_date": "2015-05-01T00:00:00Z",
                                    "average_rating": 3.0
                                  },
                                  ...
                              ]
                }

    {"success": false, "msg": "target user does not exist", ... } indicates
        the target username couldn't be found in database.
    {"success": false, "msg": "incorrect request method", ... } indicates method of the request is not GET.

    NOTE that Once successfully fetch needed information from database,
        top_reviews will contain the latest 5 reviews of the user (may be less if the user has less than 5 reveiws),
        and wishlist will contain 5 movies in the user's wishlist (may be less if the user has less than 5 movies in wishlist).
    """
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
            data['wishlist'] = list(models.Movie.objects.filter(mid__in=movie_ids).values('mid', 'name', 'region', 'released_date','average_rating','poster')[:5])

        return JsonResponse(data)
    else:
        data['msg'] = 'incorrect request method'
        return JsonResponse(data)


def my_page_view(request):
    """
    This API gets information of the logged in user.
    If the user has not logged in, it will return an error message.

    :param request: A request from frontend, the method of which is GET
    :return: A Json format data
                {
                  "success": true,
                  "msg": "",
                  "profile_photo": "a src path of user's profile photo",
                  "username" : "user's username",
                  "top_reviews":[
                                  {
                                    "user_id": a user id,
                                    "user_name": "a username",
                                    "movie_id": a movie id,
                                    "movie_name": "the name of the movie",
                                    "review_comment": "some comment here, must be a string",
                                    "rating_number": a rating number from 0 to 5, with one decimal digit,
                                    "date": "the date of review created/last edited"
                                  },
                                  {
                                    "user_id": 1,
                                    "user_name": "pete@123.com",
                                    "movie_id": 4,
                                    "movie_name": "The Avengers",
                                    "review_comment": "bad movie for movie_id = 4",
                                    "rating_number": 1.0,
                                    "date": "2020-11-05T08:13:28.537Z"
                                  },
                                  ...
                                ],
                  "wishlist": [
                                {
                                    "mid": a movie id,
                                    "name": "name fo the movie",
                                    "region": "movie's region",
                                    "released_date": "date the movie released",
                                    "average_rating": a rating number from 0 to 5, with one decimal digit,
                                    "poster": "..."
                                  },
                                  {
                                    "mid": 5,
                                    "name": "Avengers: Age of Ultron",
                                    "region": "United States",
                                    "released_date": "2015-05-01T00:00:00Z",
                                    "average_rating": 3.0,
                                    "poster": "..."
                                  },
                                  ...
                              ]
                }

    "msg" and "success" would contain following error message:

    {"success": false, "msg": "user did not log in", ... } indicates that
        the user didn't login to an account, which made the user fail to visit the user's own page.
    {"success": false, "msg": "target user does not exist", ... } indicates
        the user has already logged in, yet the username stored in session couldn't be found in database.
    {"success": false, "msg": "incorrect request method", ... } indicates method of the request is not GET.

    NOTE that once successfully fetch needed information from database,
        top_reviews will contain the latest 5 reviews of the user (may be less if the user has less than 5 reveiws),
        and wishlist will contain 5 movies in the user's wishlist (may be less if the user has less than 5 movies in wishlist).
    """
    # construct retunred data
    data = {
        'success': False,
        'msg': [],
        'profile_photo': '',
        'username': '',
        'top_reviews': [],
        'wishlist': []
    }

    if request.method == 'GET':
        # check if user has logged in and is visiting the user's own page
        if not request.session.get('login_flag', None):
            data['msg'] = 'user did not log in'
            return JsonResponse(data)

        # if the user has logged in, then get the username from session
        username = request.session.get('name', None)

        # get user object from database
        try:
            user_obj = login.models.User.objects.get(name=username)
        except ObjectDoesNotExist:
            data['msg'] = 'target user does not exist'
            return JsonResponse(data)

        data['success'] = True

        # get information needed
        if user_obj.profile_photo:
            data['profile_photo'] = str(user_obj.profile_photo)
        data['username'] = username
        reviews_list = models.Review.objects.filter(user__exact=user_obj).order_by('-date')[:5]
        for review_obj in reviews_list:
            data['top_reviews'].append(review_to_dict(review_obj))
        movie_ids = list(models.User.objects.get(name=username).wish_list_set.values('movie')[:5])
        movie_ids = [e['movie'] for e in movie_ids]
        if movie_ids:
            data['wishlist'] = list(models.Movie.objects.filter(mid__in=movie_ids).values('mid', 'name', 'region', 'released_date','average_rating','poster')[:5])

        return JsonResponse(data)

    else:
        data['msg'] = 'incorrect request method'
        return JsonResponse(data)
