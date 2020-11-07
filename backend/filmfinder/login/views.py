from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.views import APIView

from .serializers import UserSerializer
from . import models
from movies.models import Movie, Movie_genre
import simplejson

import pdb


# Create your views here.
def index_view(request):
    # Check if user has logged in
    if request.session.get('login_flag', None):
        data = {
            'login_flag': True,
            'username': request.session.get('name'),
            'most popular': []
        }
        return JsonResponse(data)
    else:
        data = {
            'login_flag': False,
            'username': None,
            'most popular': []
        }

    # Get top 10 movies based on their average ratings.
    movie_list = list(Movie.objects.order_by('-average_rating').values('mid', 'name', 'released_date', 'poster', 'average_rating')[:10])
    # Sort result based on ratings.
    data['most popular'] = sorted(list(movie_list), key=lambda x: (-x['average_rating'], x['name']))

    # pdb.set_trace()
    return JsonResponse(data)
    # return render(request, 'login/index.html')


def browse_by_genre(request):
    '''
    :param request. Input json data in this format:
                        {
                            'genre': 'A genre'
                        }
    :return:
    '''
    if request.method == 'GET':
        req = simplejson.loads(request.body)
        genre = req['genre']

        movie_list = list(Movie.objects.order_by('-average_rating').values('mid', 'name', 'released_date', 'poster', 'average_rating').filter(genre__icontains=genre)[:10])


def login_view(request):
    # Check if the user has already logged in.
    # If so, direct the user to the index page.
    if request.session.get('login_flag', None):
        data = {
            'success': False,
            'msg': 'user already logged in'
        }
        return JsonResponse(data)
        # return redirect('/index/')

    if request.method == 'POST':
        req = simplejson.loads(request.body)
        name = req['name']
        password = req['password']
        # pdb.set_trace()

        # Check if name ans password are empty
        if name and password:
            # Check if the user exists
            try:
                user = models.User.objects.get(name=name)
            except:
                data = {
                    'success': False,
                    'msg': "user doesn't exist"
                }
                return JsonResponse(data)

            # Check if the password is correct
            if user.password == password:
                # Store login information in session
                request.session['login_flag'] = True
                request.session['name'] = name
                data = {
                    'success': True,
                    'msg': None
                }
                return JsonResponse(data)
            else:
                data = {
                    'success': False,
                    'msg': 'incorrect password'
                }
                return JsonResponse(data)

        else:
            data = {
                'success': False,
                'msg': 'username and password are required'
            }
            return JsonResponse(data)

    return render(request, 'login/login.html')


def register_view(request):
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
    # Check if user didn't log in
    if request.method == 'GET':
        if not request.session.get('login_flag', None):
            data = {
                'success': False,
                'msg': "user didn't log in"
            }
            return JsonResponse(data)
            # return redirect('/index/')

    request.session.flush()
    data = {
        'success': True,
        'msg': None
    }
    return JsonResponse(data)
    # return redirect('/index/')
