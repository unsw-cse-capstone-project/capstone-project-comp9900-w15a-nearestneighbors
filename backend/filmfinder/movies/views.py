from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from . import models
from django.db.models import Avg
import simplejson
from django.http import JsonResponse
from django.core import serializers
import pdb


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

        # Get movies that keywords is or is a substring of movie names
        movie_list = list(models.Movie.objects.filter(name__icontains=key_words).values('mid', 'name', 'released_date', 'poster'))
        for movie in movie_list:
            movie['rating'] = models.Review.objects.filter(movie_id__exact=movie['mid']).aggregate(Avg('rating_number', distinct=True))['rating_number__avg']
            if movie['rating'] is not None:
                movie['rating'] = round(movie['rating'], 1)
        # pdb.set_trace()
        data = {
            'success': True,
            'result': []
        }
        # data['result'].append(serializers.serialize('python', movie_list))
        data['result'] = list(movie_list)
        return JsonResponse(data)
        # pdb.set_trace()

    return

