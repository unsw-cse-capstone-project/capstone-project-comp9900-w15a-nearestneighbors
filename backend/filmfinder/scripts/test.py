from movies.models import Movie, Review, Person
from login.models import User
from django.db.models import Avg, Count

# a = list(
#     Person.objects.get(name='Quentin Tarantino').movies.order_by('-average_rating').values('mid', 'name')[:10])

d = list(
    Person.objects.get(name='Quentin Tarantino').movie_set.order_by('-average_rating').values('mid', 'name')[:10])

# ms = d.movies.order_by('-average_rating')

print(d)
