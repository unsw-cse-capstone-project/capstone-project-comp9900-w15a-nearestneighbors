from movies.models import Movie, Review
from django.db.models import Avg, Count


def run():
    movies = Movie.objects.all()

    for movie in movies:
        reviews = movie.review.all()
        avg_rating = round(list(reviews.aggregate(Avg('rating_number')).values())[0], 1)
        count = int(list(reviews.aggregate(Count('rating_number')).values())[0])
        print(f'rating = {avg_rating}')
        print(f'count = {count}')
        movie.average_rating = avg_rating
        movie.votecount = count
        movie.save()
        print('SAVED')



