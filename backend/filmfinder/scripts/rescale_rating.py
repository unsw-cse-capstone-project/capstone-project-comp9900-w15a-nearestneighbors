from movies.models import Movie

for movie in Movie.objects.all():
    if movie.average_rating > 5:
        movie.average_rating = round(movie.average_rating / 10 * 5, 1)
        print(movie.average_rating)
        movie.save()

print('DONE')