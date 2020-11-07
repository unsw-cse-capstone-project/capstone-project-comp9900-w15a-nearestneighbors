from movies.models import Movie, Review
from django.db.models import Avg, Count

all_movies = Movie.objects.all()
for movie in all_movies:
    # genres = m.genre.all()
    # for g in genres:
    #     print(g)
    genre_list = list(movie.genre.values())
    l = ' '.join([d['genre_type'] for d in genre_list])
    print(l)
    print('---------------')

