import sklearn
import numpy as np
from numpy import genfromtxt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re
import os
from rake_nltk import Rake
import warnings
warnings.filterwarnings("ignore")


#def run():

movie_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'movie_data/IMDb movies.csv')
rating_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'movie_data/IMDb ratings.csv')

# Load data
df_info = pd.read_csv(movie_path, encoding="ISO-8859-1",
                 usecols=['imdb_title_id', 'title', 'year', 'genre', 'country', 'language', 'director', 'description'])

df_rating = pd.read_csv(rating_path, encoding="ISO-8859-1",
                 usecols=['imdb_title_id', 'weighted_average_vote', 'total_votes', 'mean_vote', 'median_vote',
                          'males_18age_avg_vote', 'males_30age_avg_vote', 'males_45age_avg_vote',
                          'females_18age_avg_vote', 'females_30age_avg_vote', 'females_45age_avg_vote'])

df_info.dropna(axis=0, how='any', inplace=True)
df_rating.dropna(axis=0, how='any', inplace=True)

df_movies = pd.merge(df_info, df_rating, how='left', on='imdb_title_id')
df_movies.dropna(axis=0, how='any', inplace=True)

r = Rake()

df_movies['keywords'] = ''

df_movies['genre'] = df_movies['genre'].map(lambda x: x.split(','))
df_movies['country'] = df_movies['country'].map(lambda x: x.split(','))
df_movies['director'] = df_movies['director'].map(lambda x: x.split(','))
for index, row in df_movies.iterrows():
    df_movies.at[index, 'genre'] = [x.lower().replace(' ', '') for x in row['genre']]
    df_movies.at[index, 'country'] = [x.lower().replace(' ', '') for x in row['country']]
    df_movies.at[index, 'director'] = [x.lower().replace(' ', '') for x in row['director']]
    r.extract_keywords_from_text(row['description'])
    keywords_dict_scores = r.get_word_degrees()
    df_movies.at[index, 'keywords'] = list(keywords_dict_scores.keys())

df_movies['bag_of_words'] = ''

columns = ['genre', 'country', 'director', 'keywords']

for index, row in df_movies.iterrows():
    words = ''
    for col in columns:
        words += ' '.join(row[col]) + ' '
    df_movies.at[index, 'bag_of_words'] = words

df_movies.sort_values(by='weighted_average_vote', ascending=False, inplace=True)

df_movies = df_movies.drop(df_movies[df_movies.total_votes < 100000].index).head(600)

# df_movies.to_csv('sorted.csv')

df_content_features = df_movies[['title', 'bag_of_words']]

df_content_features.to_csv('content_features.csv')


structured_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'content_features.csv')

df_content_features = pd.read_csv(structured_path, encoding="ISO-8859-1", usecols=['title', 'bag_of_words'])

# Calculate cosine similartity
count = CountVectorizer()
count_matrix = count.fit_transform(df_content_features['bag_of_words'])
cosine_sim = cosine_similarity(count_matrix, count_matrix)
indices = pd.Series(df_content_features['title'])
print(indices)


def recommend(title, cosine_sim=cosine_sim):
    recommended_movies = []
    idx = indices[indices == title].index[0]
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)
    top_10_indices = list(score_series.iloc[1:11].index)

    for i in top_10_indices:
        recommended_movies.append(list(df_content_features['title'])[i])

    return recommended_movies


print(recommend('The Dark Knight'))

