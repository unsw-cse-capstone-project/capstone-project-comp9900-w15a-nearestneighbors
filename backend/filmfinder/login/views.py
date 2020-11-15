from django.shortcuts import render
from django.http import JsonResponse
from . import models
from movies.models import Movie, Movie_genre, Person
import simplejson
import pdb


''' LOGIN APIS '''


def index_view(request):
    """
    This API returns most popular movies at the index page.
    If a user has logged in, then it will return the user's username.

    :param request: request.method should be GET.

    :return: A Json format data
                {
                  "login_flag": true,
                  "name": "username",
                  "most_popular":[
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

    "login_flag" indicates whether a user has logged in.
    If so, "name" will be the username. If not, "name" will be None.
    "most_popular" contains top 10 movies based on their average ratings,
        which is a list of dictionaries. In each dictionary,
        there are "mid", "name", "released_date", "poster", and "average_rating".
    """
    # Check if user has logged in
    if request.session.get('login_flag', None):
        data = {
            'login_flag': True,
            'username': request.session.get('name'),
            'most_popular': []
        }
    else:
        data = {
            'login_flag': False,
            'username': None,
            'most_popular': []
        }

    # Get top 10 movies based on their average ratings.
    movie_list = list(Movie.objects.order_by('-average_rating').values('mid', 'name', 'released_date', 'poster', 'average_rating')[:50])
    # Sort result based on ratings.
    data['most_popular'] = sorted(list(movie_list), key=lambda x: (-x['average_rating'], x['name']))

    # pdb.set_trace()
    return JsonResponse(data)
    # return render(request, 'login/index.html')


def browse_by_genre_view(request):
    """
    This API returns certain genre of movies on request.

    :param request: request contains a Json format input data
                        {
                          "genre": "a genre"
                        }
    :return: A Json format data
                {
                  "movies": [
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
    Once a user clicks buttons at index page in the section of "Browse by Genre",
    this API will return the top 10 movies based on their ratings with the requested genre.
    """
    if request.method == 'GET':
        # get data from request
        try:
            req = simplejson.loads(request.body)
            genre = req['genre']
        except:
            genre = request.GET.get('genre')

        data = {
            'movies': []
        }

        # get movies with the requested genre
        movie_list = list(Movie.objects.order_by('-average_rating').values('mid', 'name', 'released_date', 'poster', 'average_rating').filter(genre__icontains=genre)[:30])
        # sort results based on ratings
        # if two are the same then sort results alphabetically
        data['movies'] = sorted(list(movie_list), key=lambda x: (-x['average_rating'], x['name']))

        return JsonResponse(data)


def browse_by_director_view(request):
    """
    This API returns movies of a certain director on request.

    :param request: request contains a Json format data
                        {
                          "director": "a director name"
                        }
    :return: A Json format data
                {
                  "movies": [
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
    Once a user clicks buttons at index page in the section of "Browse by Director",
        this API will return the top 10 movies of the requested director based on their ratings.
    """
    if request.method == 'GET':
        # get data from request
        try:
            req = simplejson.loads(request.body)
            name = req['director']
        except:
            name = request.GET.get('director')

        # construct returned data
        data = {
            'movies': []
        }
        # get movies made by the requested director
        movie_list = list(Person.objects.get(name=name).movie_set.order_by('-average_rating').values('mid', 'name', 'released_date', 'poster', 'average_rating')[:20])
        # sort results based on ratings.
        # if two are the same then sort results alphabetically.
        data['movies'] = sorted(list(movie_list), key=lambda x: (-x['average_rating'], x['name']))

        return JsonResponse(data)


def login_view(request):
    """
    This API handles data from frontend when a user tries to log in with an account.

    :param request: request contains a Json format input data
                        {
                          "name": "username",
                          "password": "password"
                        }
    :return: A Json format data
            {
              "success": true,
              "msg": "This is login message",
              "user_id": a user id,
              "username": "a username"
            }

    "success" indicates whether a user successfully logged in. "msg" contains error messages if "success" is false, which are:
        { "success": False, "msg": "user already logged in"} indicates the user has already logged in.
        { "success": False, "msg": "tuser doesn't exist"} indicates the input username doesn't exist in our database.
        { "success": False, "msg": "incorrect password"} indicates the user didn't input correct password.
        { "success": False, "msg": "username and password are required"} indicates the user didn't input password and username.
        { "success": true, "msg": None} indicates the user successfully logged in.
    """

    if request.method == 'POST':
        # get data from request
        req = simplejson.loads(request.body)
        name = req['name']
        password = req['password']

        # check if name ans password are empty
        if name and password:
            # check if the user exists
            try:
                user = models.User.objects.get(name=name)
            except:
                data = {
                    'success': False,
                    'msg': "user doesn't exist",
                    'user_id': '',
                    'username': name
                }
                return JsonResponse(data)

            # check if the password is correct
            if user.password == password:

                # check if the user has already logged in.
                # if so, direct the user to the index page.
                if request.session.get('login_flag', None):
                    data = {
                        'success': False,
                        'msg': 'user already logged in',
                        'user_id': user.uid,
                        'username': name
                    }
                    return JsonResponse(data)
                    # return redirect('/index/')

                # store login information in session
                request.session['login_flag'] = True
                request.session['name'] = name
                data = {
                    'success': True,
                    'msg': None,
                    'user_id': user.uid,
                    'username': name
                }
                return JsonResponse(data)
            else:
                data = {
                    'success': False,
                    'msg': 'incorrect password',
                    'user_id': user.uid,
                    'username': name
                }
                return JsonResponse(data)

        # if username and password are empty, return an error message
        else:
            data = {
                'success': False,
                'msg': 'username and password are required',
                'user_id': '',
                'username': ''
            }
            return JsonResponse(data)

    return render(request, 'login/login.html')


def register_view(request):
    """
    This API handles registration information from frontend, storing them in the database.

    :param request: request contains a Json format data
                        {
                          "name": "username",
                          "password": "password",
                          "re_password": "password"
                        }
    :return: A Json format data
                {
                  "success": true,
                  "msg": "This is registration message."
                }
    "success" indicates whether a user successfully registered a new account.
    "msg" contains error messages if "success" is false, which are:

    { "success": false, "msg": "user already logged in"} indicates the user has already logged in with an existing account.
    { "success": false, "msg": "two passwords are not the same"} indicates the user didn't input the same password twice.
    { "success": false, "msg": "user already exists"} indicates the input username already exists in our database.
    { "success": true, "msg": None} indicates the user successfully registered a new account.

    """
    # Check if user has already logged in.
    # If so, direct the user to the index page.
    if request.session.get('login_flag', None):
        data = {
            'success': False,
            'msg': 'user already logged in'
        }
        return JsonResponse(data)

    if request.method == 'POST':
        req = simplejson.loads(request.body)
        username = req['name']
        password = req['password']
        re_password = req['re_password']

        # Check if two passwords are the same
        if password != re_password:
            data = {
                'success': False,
                'msg': 'two passwords are not the same'
            }
            return JsonResponse(data)
            # return render(request, 'login/register.html', {'message': message})

        # Check if username already exists
        check_user_name = models.User.objects.filter(name=username)
        if len(check_user_name) > 0:
            data = {
                'success': False,
                'msg': 'username already exists'
            }
            return JsonResponse(data)

        new_user = models.User()
        new_user.name = username
        new_user.password = password
        new_user.save()
        data = {
            'success': True,
            'msg': None
        }
        return JsonResponse(data)
        # return redirect('/login/')

    return render(request, 'login/register.html')


def logout_view(request):
    """
    This API handles user logout request by flushing user's session.

    :param request: the method of request should be GET.

    :return: A Json format data
                {
                  "success": true,
                  "msg": "This is registeration message."
                }

    "success" indicates whether a user successfully logged out.
    "msg" contains error message if "success" is false,
        which is { "success": false, "msg": "user didn't log in"} indicates the user didn't logged in with an existing account.
    { "success": true, "msg": None} indicates the user successfully logged out, and the session has been flushed.
    """
    if request.method == 'GET':
        # check if user has logged in
        if not request.session.get('login_flag', None):
            data = {
                'success': False,
                'msg': "user didn't log in"
            }
            return JsonResponse(data)

    # flush session if the user has logged in
    request.session.flush()
    data = {
        'success': True,
        'msg': None
    }
    return JsonResponse(data)

