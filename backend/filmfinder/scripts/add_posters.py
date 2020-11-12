from movies.models import Movie, Person, Movie_genre
import pandas as pd
import os


def run():
    movie_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Sri_database/moviesfinal.csv')
    df_movie = pd.read_csv(movie_path, encoding="ISO-8859-1", usecols=['movie_id', 'Movie_name'])
    # ../movies/posters/LOTRFOTRmovie.jpg
    parent_dir = '../movies/posters/'
    count = 0
    for index, row in df_movie.iterrows():
        if len(list(Movie.objects.filter(name__exact=row['Movie_name']).values_list('name'))) > 0:
            movie_obj = Movie.objects.get(name=row['Movie_name'])
            print(row['Movie_name'], row['movie_id'], movie_obj.poster)
            if movie_obj.poster == '':
                pic = str(row['movie_id']) + '.jpg'
                movie_obj.poster = parent_dir + pic
                movie_obj.save()
                count += 1
    print('DONE')
    print(count)

