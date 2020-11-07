from movies.models import Movie, Review
from django.db.models import Avg, Count

all_movies = Movie.objects.all()
for movie in all_movies:
    genres = ' '.join([d['genre_type'] for d in list(movie.movie_genre.values())])
    movie.genre = genres
    movie.save()
    print(genres)
    print('---------------')

