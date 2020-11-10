import sklearn
import numpy as np
from numpy import genfromtxt
from movies.models import Movie, Person, MovieFeatures
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re
import os
from rake_nltk import Rake
import warnings
warnings.filterwarnings("ignore")


def run():

    r = Rake()

    movies = Movie.objects.all()

    for movie in movies:
        title = movie.name
        description = movie.description
        r.extract_keywords_from_text(description)
        keywords_dict_scores = r.get_word_degrees()
        keywords = list(keywords_dict_scores.keys())
        region = [x.lower().replace(' ', '') for x in movie.region.split(',')]
        genre = [x.lower().replace(' ', '') for x in movie.genre.split(',')]
        director_name = Person.objects.get(pid=movie.director_id).name.split(',')
        director = [x.lower().replace(' ', '') for x in director_name]
        bag_of_words = ' '.join(director) + ' ' + ' '.join(genre) + ' ' + ' '.join(region) + ' ' + ' '.join(keywords)
        MovieFeatures.objects.create(movie=movie, title=title, bag_of_words=bag_of_words)
        # print([title, description, region, genre, director])

    print('DONE')

