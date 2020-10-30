from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.views import APIView

from .serializers import UserSerializer
from . import models, forms


# DRL API - Implemented with serializers
class LoginView(APIView):

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return JsonResponse(serializer.data)


    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)



# Create your views here.
def index_view(request):
    # Validate login status
    if not request.session.get('login_flag', None):
        return redirect('/login/')
    return render(request, 'index.html')


def login_view(request):
    # Check if the user has already logged in
    if request.session.get('login_flag', None):
        return redirect('/index/')

    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        # Check if name ans password are empty
        if name and password:
            print(name, password)

            # Check if the user exists
            try:
                user = models.User.objects.get(name=name)
            except:
                message = "user doesn't exist"
                return render(request, 'login.html', {'message': message})

            # Check if the password is correct
            if user.password == password:
                # Store login information in session
                request.session['login_flag'] = True
                request.session['name'] = name
                return redirect('/index/')
            else:
                message = 'password is incorrect'
                return render(request, 'login.html', {'message': message})

    return render(request, 'login.html')


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
    # Check if user has already logged in
    if request.session.get('login_flag', None):
        return redirect('/index/')

    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        email = request.POST.get('email')

        check_user_name = models.User.objects.get(name=name)
        if check_user_name == name:
            message = 'User already exists!'
            return render(request, 'register.html', {'message': message})

        check_email = models.User.objects.get(name=email)
        if check_email == email:
            message = 'This email has been registered!'
            return render(request, 'register.html', {'message': message})

        new_user = models.User()
        new_user.name = name
        new_user.password = password
        new_user.email = email
        new_user.save()

        return redirect('/login/')

    return render(request, 'register.html')


def logout_view(request):
    # Check if user didn't log in
    if not request.session.get('login_flag', None):
        return redirect('/index/')

    request.session.flush()
    return redirect('/login/')
