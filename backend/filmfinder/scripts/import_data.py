from movies.models import Movie, Person, Movie_genre
import pandas as pd
import os
import urllib


# print(os.path.isfile('/movies/Movie.csv'))
def run():
    movie_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Sri_database/Movie.csv')
    person_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Sri_database/Person.csv')
    genre_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Sri_database/Movie_Genre.csv')
    tmdb_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Sri_database/tmdb_5000_movies.csv')
    poster_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Sri_database/Movie_Poster.csv')
    download_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'posters/')

    df_movie = pd.read_csv(movie_path, encoding="ISO-8859-1",
                     usecols=['mid', 'name', 'region', 'released_date', 'director', 'rating', 'votecount'])
    df_movie.rename(columns={'votecount': 'average_rating'}, inplace=True)
    df_movie.rename(columns={'rating': 'votecount'}, inplace=True)

    df_person = pd.read_csv(person_path, encoding="ISO-8859-1",
                     usecols=['pid', 'name'])

    df_genre = pd.read_csv(genre_path, encoding="ISO-8859-1",
                     usecols=['movie', 'genretype', 'genreid'])

    df_tmdb = pd.read_csv(tmdb_path, encoding="ISO-8859-1",
                     usecols=['id', 'overview'])

    df_poster = pd.read_csv(poster_path, encoding="ISO-8859-1",
                          usecols=['imdbId', 'Poster', 'Imdb Link'])

    # Create Person objects
    # for index, row in df_person.iterrows():
    #     if not Person.objects.filter(name__exact=row['name']):
    #         Person.objects.create(name=row['name'])

    #Create movie objects
    for index, row in df_movie.iterrows():
        # If movie is not in current database
        if not Movie.objects.filter(name__exact=row['name']):

            genre_list = list(df_genre.loc[df_genre['movie'] == row['mid']]['genretype'])
            d_name = list(set(list(df_person.loc[df_person['pid'] == row['director']]['name'])))
            description = list(df_tmdb.loc[df_tmdb['id'] == row['mid']]['overview'])[0]
            poster_dir = ''
            d_id = list(Person.objects.filter(name__exact=d_name[0]).values('pid'))[0]['pid']

            # Download posters
            poster_link = list(df_poster.loc[df_poster['imdbId'] == row['mid']]['Poster'])
            if poster_link:
                poster_name = row['name'].replace(' ', '_') + '.jpg'
                poster_dir = '../ movies / posters / ' + poster_name
                # print(f"NAME: {row['name']}  {row['mid']}\nPOSTER: {poster_name}\n")
                # file_path = download_path + poster_name
                # try:
                #     urllib.request.urlretrieve(poster_link[0], file_path)
                # except:
                #     print('ERROR')
                #     pass

            Movie.objects.create(name=row['name'], description=description, region=row['region'],
                                 released_date=row['released_date'], poster=poster_dir, average_rating=row['average_rating'],
                                 votecount=row['votecount'], genre=' '.join(genre_list).replace('Fiction', 'fiction'),
                                 director_id=d_id)

            # Create Movie_genre objects
            for genre in genre_list:
                if 'Fiction' in genre:
                    genre = genre.replace('Fiction', 'fiction')
                Movie_genre.objects.create(movie_id=Movie.objects.get(name=row['name']).mid, genre_type=genre)


    print('DONE')

