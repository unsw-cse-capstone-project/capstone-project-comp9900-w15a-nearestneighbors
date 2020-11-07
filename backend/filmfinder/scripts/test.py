from movies.models import Movie, Review, Person
from django.db.models import Avg, Count


d = list(Person.objects.filter(name__icontains='quentin').movies.order_by('-average_rating').values('mid', 'name', 'released_date', 'poster', 'average_rating')[:10])


# ms = d.movies.order_by('-average_rating')

print(d)


