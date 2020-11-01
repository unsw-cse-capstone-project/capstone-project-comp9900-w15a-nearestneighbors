from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from . import models
import simplejson
from django.http import JsonResponse


# Create your views here.
def index(request):
    #return HttpResponse("Hello, world. You're at the movies index.")
    movie_list = models.Movie.objects.order_by('name')[:]
    context = {"movie_list": movie_list}
    return render(request, 'movies/index.html', context)
    
    
def detail(request,movie_id):
    movie = get_object_or_404(models.Movie, pk = movie_id)
    return render(request, 'movies/detail.html', {'movie': movie})


def search_view(request):
    if request.method == 'GET':
        req = simplejson.loads(request.body)
        key_words = req['keywords'].strip()

        # Check if input is empty
        if not key_words:
            data = {
                'success': False,
                'msg': 'empty input'
            }
            return JsonResponse(data)

        # Get movies that keywords is or is a substring of movie names
        movie_list = models.Movie.objects.filter(title__icontains=key_words)
        # Search for movies, the name of which matches input keywords
        movie_list = models.Movie.objects.filter(title__icontains=q)

        # pdb.set_trace()

    return

