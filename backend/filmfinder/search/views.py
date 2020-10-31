from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.views import APIView

import pdb


# Create your views here.
def search_view(request):
    key_words = request.GET.get('search')
    # Check if input is empty
    if not key_words:
        message = 'Please input a key word!'
        return render(request, 'login/index.html', {'message': message})
    pdb.set_trace()


    return redirect('/login/')

