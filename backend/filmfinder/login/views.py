from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.views import APIView

from .serializers import UserSerializer
from . import models, forms

import pdb

# DRL API - Implemented with serializers
# class LoginView(APIView):
#
#     def get(self, request, *args, **kwargs):
#         queryset = User.objects.all()
#         serializer = UserSerializer(queryset, many=True)
#         return JsonResponse(serializer.data)
#
#
#     def post(self, request, *args, **kwargs):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)


# Create your views here.
def index_view(request):
    # Check if user has logged in
    if request.session.get('login_flag', None):
        message = request.session.get('name') + ', Welcome back! '
        return render(request, 'login/index.html', {'message': message})
    # Validate login status
    return render(request, 'login/index.html')


def login_view(request):
    # pdb.set_trace()
    # Check if the user has already logged in.
    # If so, direct the user to the index page.
    if request.session.get('login_flag', None):
        data = {
            'success': False,
            'msg': 'User already logged in'
        }
        return JsonResponse(data)
        # return redirect('/index/')

    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        # pdb.set_trace()
        # Check if name ans password are empty
        if name and password:
            # Check if the user exists
            try:
                user = models.User.objects.get(name=name)
            except:
                message = "user doesn't exist"
                data = {
                    'success': True,
                    'msg': None
                }
                # return render(request, 'login/login.html', {'message': message})
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
                # return redirect('/index/')
            else:
                message = 'password is incorrect'
                data = {
                    'success': False,
                    'msg': 'password is incorrect'
                }
                return JsonResponse(data)
                # return render(request, 'login/login.html', {'message': message})
        else:
            data = {
                'success': False,
                'msg': 'username and password are required'
            }
            return JsonResponse(data)
            # return redirect('/index/')

    elif request == 'GET':

        data = {
            'success': None,
            'msg': 'GET request'
        }

        return JsonResponse(data)
    # pdb.set_trace()
    data = {
        'success': False,
        'msg': 'unexpected request'
    }
    return JsonResponse(data)
    # return render(request, 'login/login.html')


''' If Forms is used '''
# def login_view(request):
#     if request.method == 'POST':
#         login_form = forms.UserForm(request.POST)
#         if login_form.is_valid():
#             name = login_form.cleaned_data.get('name')
#             password = login_form.cleaned_data.get('password')
#             print(name, password)
#             try:
#                 user = models.User.objects.get(name=name)
#             except:
#                 message = "user doesn't exist"
#                 return render(request, 'login.html', {'message': message})
#             if user.password == password:
#                 return redirect('/index/')
#             else:
#                 message = 'password is incorrect'
#                 return render(request, 'login.html', {'message': message})
#         else:
#             message = 'login form is invalid'
#             return render(request, 'login.html', {'message': message})
#     login_form = forms.UserForm()
#     return render(request, 'login.html')


def register_view(request):
    # Check if user has already logged in.
    # If so, direct the user to the index page.
    if request.session.get('login_flag', None):
        return redirect('/index/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('userPassword')
        re_password = request.POST.get('userRePassword')
        # email = request.POST.get('email')

        # Check if two passwords are the same
        if password != re_password:
            message = 'Please input two same passwords!'
            return render(request, 'login/register.html', {'message': message})

        # Check if username already exists
        check_user_name = models.User.objects.filter(name=username)
        # pdb.set_trace()
        if len(check_user_name) > 0:
            message = 'User already exists!'
            return render(request, 'login/register.html', {'message': message})

        new_user = models.User()
        new_user.name = username
        new_user.password = password
        new_user.save()

        return redirect('/login/')

    return render(request, 'login/register.html')


def logout_view(request):
    # Check if user didn't log in
    if not request.session.get('login_flag', None):
        return redirect('/index/')

    request.session.flush()
    return redirect('/index/')
