from movies.models import Movie, Review, Person
from django.db.models import Avg, Count


d = Review.objects.get(user=4, movie=5).rating_number


# ms = d.movies.order_by('-average_rating')

print(d)
print(type(d))


