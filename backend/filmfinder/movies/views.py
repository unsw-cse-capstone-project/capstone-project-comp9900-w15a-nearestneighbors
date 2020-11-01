from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from . import models
# Create your views here.

def index(request):
    #return HttpResponse("Hello, world. You're at the movies index.")
    movie_list = models.Movie.objects.order_by('name')[:]
    context = {"movie_list": movie_list}
    return render(request,'movies/index.html',context)
    
    
def detail(request,movie_id):
    movie = get_object_or_404(models.Movie, pk = movie_id)
    return render(request, 'movies/detail.html', {'movie': movie})


def search(request):
    key_words = request.GET.get('search')
    # Check if input is empty
    if not key_words:
        message = 'Please input a key word!'
        return render(request, 'login/index.html', {'message': message})
    pdb.set_trace()
    return

