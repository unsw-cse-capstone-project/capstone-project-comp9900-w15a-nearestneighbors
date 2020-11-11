from login.models import User
from movies.models import Movie, User_banned_list
import numpy as np


def run():
    for uid in range(1, 53):
        user_obj = User.objects.get(uid=uid)
        banned_uid = np.random.randint(low=1, high=53, size=np.random.randint(low=0, high=5))
        if len(banned_uid) > 0:
            for banned in banned_uid:
                banned_obj = User.objects.get(uid=banned)
                try:
                    User_banned_list.objects.create(user=user_obj, banned_user=banned_obj)
                except:
                    continue

    print('DONE')
