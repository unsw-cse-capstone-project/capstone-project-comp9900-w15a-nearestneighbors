from login.models import User
from movies.models import Movie, Wish_list
import numpy as np
from faker import Faker


def run():
    email = ['@outlook.com', '@hotmail.com', '@yahoo.com', '@qq.com', '@gmail.com', '@msn.com', '@mail.com']
    faker = Faker()
    for i in range(0, 30):
        name = faker.name().replace(" ", "_").lower() + email[np.random.randint(low=0, high=6)]
        password = str(np.random.randint(low=0, high=9)) * 6
        User.objects.create(name=name, password=password, email=name, profile_photo='')
    print('DONE')

