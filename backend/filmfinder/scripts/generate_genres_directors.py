from django.db.models import Count
from movies.models import Movie, Movie_genre,Person


def run():
    top_directors = list(Movie.objects.values_list('director', flat=True).annotate(Count('director')).order_by('-director__count')[:10])
    for did in top_directors:
        print(Person.objects.get(pid=did).name)
    all_genres = list(Movie_genre.objects.order_by('genre_type').values_list('genre_type', flat=True).distinct())
    for g in all_genres:
        print(g)

