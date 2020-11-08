from movies.models import Movie, Review, Person
from login.models import User
from django.db.models import Avg, Count


d = Movie.objects.get(mid=5).poster
a = User.objects.get(name='1@1.1').profile_photo


# ms = d.movies.order_by('-average_rating')

print(d)
if a:
    print('not none')
else:
    print('none')

