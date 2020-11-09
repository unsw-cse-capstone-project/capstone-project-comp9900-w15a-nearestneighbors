from movies.models import Movie, Review, Person
from login.models import User
from django.db.models import Avg, Count

# a = list(
#     Person.objects.get(name='Quentin Tarantino').movies.order_by('-average_rating').values('mid', 'name')[:10])
def run():
    a = 'Family'
    b = 'Science Fiction'

    print('Fiction' in a)
    print('Fiction' in b)