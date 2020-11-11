from login.models import User
from movies.models import Movie, Wish_list
import numpy as np


def run():
    for mid in range(4, 216):
        uid = set(np.random.randint(low=24, high=53, size=12))
        movie_obj = Movie.objects.get(mid=mid)
        for user in uid:
            user_obj = User.objects.get(uid=user)
            try:
                Wish_list.objects.create(movie=movie_obj, user=user_obj)
            except:
                continue

    print('DONE')
