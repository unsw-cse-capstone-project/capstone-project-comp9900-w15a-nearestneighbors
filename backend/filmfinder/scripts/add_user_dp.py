from login.models import User
import pandas as pd
import os


def run():
    default_dp = '../movies/user_dp/default.png'
    count = 0
    all_users = User.objects.all()
    for user in all_users:
        user.profile_photo = default_dp
        user.save()
        count += 1
    print('DONE')
    print(count)

