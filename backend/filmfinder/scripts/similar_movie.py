import sklearn
import numpy as np
from numpy import genfromtxt
import pandas as pd
import re

# Load data
df_info = pd.read_csv('movie_data/IMDb movies.csv', encoding="ISO-8859-1",
                 usecols=['imdb_title_id', 'title', 'year', 'genre', 'country', 'language', 'director'])

df_rating = pd.read_csv('movie_data/IMDb ratings.csv', encoding="ISO-8859-1",
                 usecols=['imdb_title_id', 'weighted_average_vote', 'total_votes', 'mean_vote', 'median_vote',
                          'males_18age_avg_vote', 'males_30age_avg_vote', 'males_45age_avg_vote',
                          'females_18age_avg_vote', 'females_30age_avg_vote', 'females_45age_avg_vote'])


df_info.dropna(axis=0, how='any', inplace=True)
df_rating.dropna(axis=0, how='any', inplace=True)

df_movies = pd.merge(df_info, df_rating, how='left', on='imdb_title_id')
df_movies.dropna(axis=0, how='any', inplace=True)

print(df_movies)

df['Genre'] = df['Genre'].map(lambda x: x.split(','))
df['Actors'] = df['Actors'].map(lambda x: x.split(',')[:3])
df['Director'] = df['Director'].map(lambda x: x.split(','))for index, row in df.iterrows():
    row['Genre'] = [x.lower().replace(' ','') for x in row['Genre']]
    row['Actors'] = [x.lower().replace(' ','') for x in row['Actors']]
    row['Director'] = [x.lower().replace(' ','') for x in row['Director']]
