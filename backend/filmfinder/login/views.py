from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect
from . import models
from . import forms


# Create your views here.
def index_view(request):
    pass
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        if name and password:
            print(name, password)
            try:
                user = models.User.objects.get(name=name)
            except:
                message = "user doesn't exist"
                return render(request, 'login.html', {'message': message})
            if user.password == password:
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
    pass
    return render(request, 'register.html')


def logout_view(request):
    pass
    return redirect('login.html')
