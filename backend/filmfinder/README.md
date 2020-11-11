# Django APIs

## Login

### index_view

**Author**: PATRICK LI

**Url**:  http://127.0.0.1:8000/index/

**Request Method**: GET

**Input Request**:  N/A

**Output Data**:
```
{
  "login_flag": true,
  "name": "username",
  "most_popular":[
              {
              "mid": "movie id", 
              "name": "movie name", 
              "released_date": "released year", 
              "poster": "src path of poster", 
              "average_rating": "latest averaged rating"
            },
              {
              "mid": "movie id", 
              "name": "movie name", 
              "released_date": "released year", 
              "poster": "src path of poster", 
              "average_rating": "latest averaged rating"
            },
              ...
          ]
}
```
`"login_flag"` indicates whether a user has logged in. 
If so, `"name"` will be the username. 
If not, `"name"` will be `None`.
`"most_popular"` contains ***top 10*** movies based on their average ratings, which is a list of dictionaries. In each dictionary, there are `"mid"`, `"name"`, `"released_date"`, `"poster"`, and `"average_rating"`.

:warning: ***The output data structure has changed, compared with the previous version.*** :warning:


<br/><br/>
### browse_by_genre_view

**Author**: PATRICK LI

**Url**:  http://127.0.0.1:8000/browse_by_genre/

**Request Method**: GET

**Input Request**:
```json
{
  "genre": "a genre"
}
```
**Output Data**:
```
{
  "movies": [
              {
              "mid": "movie id", 
              "name": "movie name", 
              "released_date": "released year", 
              "poster": "src path of poster", 
              "average_rating": "latest averaged rating"
            },
              {
              "mid": "movie id", 
              "name": "movie name", 
              "released_date": "released year", 
              "poster": "src path of poster", 
              "average_rating": "latest averaged rating"
            },
              ...
          ]
}
```
Once a user clicks buttons at index page in the section of "Browse by Genre", this API will return the ***top 10*** movies based on their ratings with the requested genre.


<br/><br/>
### browse_by_director_view

**Author**: PATRICK LI

**Url**:  http://127.0.0.1:8000/browse_by_director/

**Request Method**: GET

**Input Request**:
```json
{
  "director": "a director name"
}
```
**Output Data**:
```
{
  "movies": [
              {
              "mid": "movie id", 
              "name": "movie name", 
              "released_date": "released year", 
              "poster": "src path of poster", 
              "average_rating": "latest averaged rating"
            },
              {
              "mid": "movie id", 
              "name": "movie name", 
              "released_date": "released year", 
              "poster": "src path of poster", 
              "average_rating": "latest averaged rating"
            },
              ...
          ]
}
```
Once a user clicks buttons at index page in the section of "Browse by Director", this API will return the ***top 10*** movies of the requested director based on their ratings.

:warning: ***The value of input data, i.e. the value of "director", must be as the same as it stored in the database.*** :warning:

:warning:   The index_view, browse_by_genre_view and browse_by_director_view only return ***top 10*** movies now. If ***all movies*** could be displayed at frontend, please let me know. I'll adjust those three views to it.


<br/><br/>
### login_view

**Author**: PATRICK LI

**Url**:  http://127.0.0.1:8000/login/

**Request Method**: POST

**Input Request**:
```json
{
  "name": "username",
  "password": "password"
}
```

**Output Data**:
```json
{
  "success": true,
  "msg": "This is login message",
  "user_id": a user id,
  "username": "a username"
}
```
`"success"` indicates whether a user successfully logged in.
`"msg"` contains error messages if `"success"` is `false`, which are:
  1. `{ "success": False, "msg": "user already logged in"}` indicates the user has already logged in.
  2. `{ "success": False, "msg": "tuser doesn't exist"}` indicates the input username doesn't exist in our database.
  3. `{ "success": False, "msg": "incorrect password"}` indicates the user didn't input correct password.
  4. `{ "success": False, "msg": "username and password are required"}` indicates the user didn't input password and username.

`{ "success": true, "msg": None}` indicates the user successfully logged in.


<br/><br/>
### register_view

**Author**: PATRICK LI

**Url**:  http://127.0.0.1:8000/register/

**Request Method**: POST

**Input Request**:
```json
{
  "name": "username",
  "password": "password",
  "re_password": "password"
}
```
`"name"` is the username a user wants to register. 
`"password"` is user's input password.
`"re_password"` is re-entered password to confirm the password.

**Output Data**:
```json
{
  "success": true,
  "msg": "This is registeration message."
}
```
`"success"` indicates whether a user successfully registered a new account.
`"msg"` contains error messages if `"success"` is `false`, which are:
  1. `{ "success": false, "msg": "user already logged in"}` indicates the user has already logged in with an existing account.
  2. `{ "success": false, "msg": "two passwords are not the same"}` indicates the user didn't input the same password twice.
  3. `{ "success": false, "msg": "user already exists"}` indicates the input username already exists in our database.

`{ "success": true, "msg": None}` indicates the user successfully registered a new account.


<br/><br/>
### logout_view

**Author**: PATRICK LI

**Url**:  http://127.0.0.1:8000/logout/

**Request Method**: GET

**Input Request**: N/A

**Output Data**:
```json
{
  "success": true,
  "msg": "This is registeration message."
}
```
`"success"` indicates whether a user successfully logged out.
`"msg"` contains error message if `"success"` is `false`, which is `{ "success": false, "msg": "user didn't log in"}` indicates the user didn't logged in with an existing account.

`{ "success": true, "msg": None}` indicates the user successfully logged out, and the session has been flushed.
<br/><br/>
<br/><br/>



## Movies
### search_view

**Author**: PATRICK LI

**Url**:  http://127.0.0.1:8000/search/

**Request Method**: GET

**Input Request**:
```json
{
  "search": "some key words here"
}
```
`"search"` is the keywords a user input to search for movies.

**Output Data**:
```
{
  "success": true,
  "result": [
              {
              "mid": "movie id", 
              "name": "movie name", 
              "released_date": "released year", 
              "poster": "src path of poster", 
              "average_rating": "latest averaged rating"
            },
              {
              "mid": "movie id", 
              "name": "movie name", 
              "released_date": "released year", 
              "poster": "src path of poster", 
              "average_rating": "latest averaged rating"
            },
              ...
          ]
}
```
`"success"` indicates whether the input keywords can conduct a search successfully.

`"result"` contains search result, which is a list of dictionaries. In each dictionary, there are `"mid"`, `"name"`, `"released_date"`, `"poster"`, and `"average_rating"`. 

They are used to demonstrate each movie in search result, except `"mid"`.
`{ "success": true, "result": []}` indicates no related movie is found.

When searching for movies, keywords can be:
  - a movie name or a substring of a movie name;
  - a director name or a substring of a director name;  
  - a region or a substring of a region;
  - a genre or a substring of a genre;
  - Any combination of keywords mentioned above.
  
When input keywords are multiple constraints, the search will be conducted based on a conjunction of input keywords. For example, if input keywords are `UK 2003 quentin`, it will search for Quentin Tarantino's movies made in UK in 2003.


<br/><br/>
### movie_list_view
**Author**: ZIJAN SHEN

**Url**:  http://127.0.0.1:8000/movies/

**Request Method**: GET

**Input Request**: No Input

**Output Data**:
```
{
"success": true,
"movies":[
            {
              "mid": 1,
              "name": "test_movie1",
              "genre":[
                "test_genre1",
                "test_genre12",
                "test_genre3"
              ],
              "description": "test_movie1_description",
              "region": "US",
              "released_date": "2020-10-30T09:37:52Z",
              "director": "test_director1",
              "poster": "../movies/posters/壁纸.jpg",
              "cast":[
                "test_actor1",
                "test_actor2"
              ],
              "average_rating":4.5
            },

            {
              "mid": 2,
              "name": "test_movie2",
              "genre":["test_genre1", "test_genre3"],
              "description": "test_movie2 description",
              "region": "SYD",
              "released_date": "2020-10-05T00:00:00Z",
              "director": "test_director2",   
              "poster": "../movies/posters/终将成为你6.jpg",
              "cast":["test_actor1"],
              "average_rating":4.3
            },

            ...

            {
              ...
            },

          ]
}
```
return all movies detail for all movie objects in database.

`"success"` indicates `http://127.0.0.1:8000/movies/` successfully return all movies.

`"movies"` contains search result, which is a list of dictionaries. 

In each dictionary, there are `"mid"`, `"name"`, `"genre type"`,`"description"`,`"region"`,  `"released_date"`,`"director_name"`,`"poster"`,`"cast"`,`"average_rating"` fields.

Note that if the user is logged in, the `"average_rating"` field will exclude reviews given by users in banned list.


<br/><br/>
### detail_view
**Author**: ZIJIAN SHEN

**Url**:  http://127.0.0.1:8000/movies/detail/

**Request Method**: GET

**Input Request**:
```json
{
  "movie_id": "some movie id here, must be a positive integer"
}
```

**Output Data**:
```
{
  "success": true/false,
  "msg": "some message here"
  "movies": [
    {
      'mid': 4,
      'name': 'The Avengers',
      'genre': ['Action', 'Adventure', 'Science fiction'],
      'description': "Marvel's The Avengers[6] (classified under the name .....",
      'region': 'United States',
      'released_date': datetime.datetime(2012, 5, 4, 12, 0, tzinfo=<UTC>),
      'director': 'Joss Whedon',
      'poster': '../movies/posters/The_Avengers_2012_film_poster.jpg',
      'cast': [
                  'Robert Downey Jr.',
                  'Chris Evans',
                  'Mark Ruffalo',
                  'Chris Hemsworth',
                  'Scarlett Johansson',
                  'Jeremy Renner',
                  'Tom Hiddleston'
              ],
      'average_rating': 4.5,
      'reviews':[
                  {
                      'user_id': 6,
                      'user_name': '6@6.6',
                      'review_comment': 'I was lucky enough to attend the Marve.....',
                      'rating_number': 4.5,
                      'date': datetime.datetime(2018, 4, 11, 6, 41, 19, tzinfo=<UTC>)
                  },
                  {
                      'user_id': 5,
                      'user_name': '5@5.5',
                      'review_comment': "'Avengers Assemble' ('The Avengers') is a truly enjoyable superhero film that ....",
                      'rating_number': 5.0,
                      'date': datetime.datetime(2015, 11, 4, 6, 40, 34, tzinfo=<UTC>)
                  },
                  {
                      'user_id': 7,
                      'user_name': '7@7.7',
                      'review_comment': "I just saw the early screening for San Diego through the top 10 cities on facebook who got them.....",
                      'rating_number': 4.7,
                      'date': datetime.datetime(2012, 12, 30, 6, 41, 53, tzinfo=<UTC>)
                  }
              ]
    }
  ]
  "similar_movies": [
              {
              "mid": "movie id", 
              "name": "movie name", 
              "released_date": "released year", 
              "poster": "src path of poster", 
              "average_rating": "latest averaged rating"
            },
              {
              "mid": 5, 
              "name": "Avengers: Age of Ultron", 
              "released_date": "2015-05-01T00:00:00Z", 
              "poster": "src path of poster", 
              "average_rating": 3.0
            },
              ...
          ]
}
```
get a movie detail by giving movie_id.

`"success"` indicates whether found matching movie.

`"msg"` shows the current state.

`"movie"` is a list, which has only one element, containing detail for the matching movie.

1. `{"success": false, "msg": "movie_id is required", "movie": []}` indicates there is no input in the GET Query Parameters.
2. `{"success": false, "msg": "movie_id must be a positive integer", "movie": []}` indicates the input is not a positive integer.
3. `{"success": false, "msg": "does not have movie with movie_id: " + str(movie_id), "movie": []}` indicates there is no movie with mid == movie_id
4. `{"success": true, "msg": "found movie with movie_id: " + str(movie_id), "movie": [{...}]}` indicates there is a movie with mid == movie_id

Note that if the user is logged in, the `"reviews"` field will exclude reviews given by users in banned list.


<br/><br/>
### add_to_wishlist_view

**Author**: ZIJIAN SHEN

**Url**: http://127.0.0.1:8000/movies/detail/add_to_wishlist/

**Request Method**: GET

**Input Request**:
```json
{
  "movie_id": "some movie id here, must be a positive integer"
}
```
**Output Data**:
```
{
  "success": true/false,
  "msg": "some message here"
}
```
add movie given by movie_id to user's wish_list.

1. `{"success": false, "msg": "user does not log in"}` indicates that user does not log in
2. `{"success": false, "msg": "movie_id is required"}` means the input json dose not have movie_id field
3. `{"success": false, "msg": "movie_id must be a positive integer"}` indicates the input json does not follow the above input request
4. `{"success": false, "msg": "does not have movie with movie_id: " + str(movie_id)}` indicates the given movie_id field does not match any record in Movie database
5. `{"success": false, "msg": "movie already in wishlist"}` indicates the given movie is already in wishlist
6. `{"success": true, "msg": "successfully insert movie to wishlist"}` indicates the given movie is successfully inserted into wishlist


<br/><br/>
### all_reviews_view

**Author**: ZIJIAN SHEN

**Url**:  http://127.0.0.1:8000/movies/detail/all_reviews/

**Request Method**: GET

**Input Request**:
```json
{
  "movie_id": "some movie id here, must be a positive integer"
}
```

**Output Data**:
```
{
  "success": true/false,
  "msg": "some message here"
  "reviews":[
              {
                  'user_name': '6@6.6',
                  'review_comment': 'I was lucky enough to attend the Marve.....',
                  'rating_number': 4.5,
                  'date': datetime.datetime(2018, 4, 11, 6, 41, 19, tzinfo=<UTC>)
              },
              {
                  'user_name': '5@5.5',
                  'review_comment': "'Avengers Assemble' ('The Avengers') is a truly enjoyable superhero film that ....",
                  'rating_number': 5.0,
                  'date': datetime.datetime(2015, 11, 4, 6, 40, 34, tzinfo=<UTC>)
              },
              {
                  'user_name': '7@7.7',
                  'review_comment': "I just saw the early screening for San Diego through the top 10 cities on facebook who got them.....",
                  'rating_number': 4.7,
                  'date': datetime.datetime(2012, 12, 30, 6, 41, 53, tzinfo=<UTC>)
              }
            ]
}
```
get all reviews by giving movie_id.

`"success"` indicates whether successfully return all reviews.

`"msg"` shows the current state.

1. `{"success": false, "msg": "movie_id is required", "reviews": []}` indicates there is no input in the GET Query Parameters.
2. `{"success": false, "msg": "movie_id must be a positive integer", "reviews": []}` indicates the input is not a positive integer.
3. `{"success": false, "msg": "does not have movie with movie_id: " + str(movie_id), "reviews": []}` indicates there is no movie with mid == movie_id
4. `{"success": true, "msg": "found all reviews for movie_id: " + str(movie_id), "reviews": [{...}, {...}]}` indicates there is a movie with mid == movie_id, and found all reviews for this movie.

Note that if the user is logged in, the `"reviews"` field will exclude reviews given by users in banned list.


<br/><br/>
### new_review_view

**Author**: ZIJIAN SHEN

**Url**:  http://127.0.0.1:8000/movies/detail/new_review/

**Request Method**: POST

**Input Request**:
```json
{
  "movie_id": "some movie id here, must be a positive integer", 
  "review_comment": "some comment here, must be a string",
  "rating_number": "some rating number here, must be a positive number"
}
```

**Output Data**:
```
{
  "success": true/false
  "msg": "some message here",
}
```

`"success"` indicates whether successfully create new review.

`"msg"` shows the current state.

1. `{"success": false, "msg": "user does not log in"}` indicates that user does not log in
2. `{"success": false, "msg": "movie_id, review_comment, rating_number are required"}` means the input json dose not have either movie_id field, or review_comment field, or rating_number field
3. `{"success": false, "msg": "movie_id must be a positive integer, review_comment must be a string, rating_number must be a positive number"}` indicates the input json does not follow the above input request
4. `{"success": false, "msg": "does not have movie with movie_id: " + str(movie_id)}` indicates the given movie_id field does not match any record in Movie database
5. `{"success": false, "msg": "each user can only leave one review for a movie, but reviews are editable"}` indicates that there is already a review for the current user and the given movie
6. `{"success": true, "msg": "successfully create a new review"}` indicates a new review is created
<br/><br/>
<br/><br/>



## My Page

### my_page_view

**Author**: PATRICK LI

**Url**: http://127.0.0.1:8000/my_page/

**Request Method**: GET

**Input Request**: N/A

**Output Data**: 
```
{
  "success": true,
  "msg": "",
  "profile_photo": "a src path of user's profile photo",
  "username" : "user's username",
  "top_reviews":[
                  {
                    "user_id": a user id,
                    "user_name": "a username",
                    "movie_id": a movie id,
                    "movie_name": "the name of the movie",
                    "review_comment": "some comment here, must be a string",
                    "rating_number": a rating number from 0 to 5, with one decimal digit,
                    "date": "the date of review created/last edited"
                  },
                  {
                    "user_id": 1,
                    "user_name": "pete@123.com",
                    "movie_id": 4,
                    "movie_name": "The Avengers",
                    "review_comment": "bad movie for movie_id = 4",
                    "rating_number": 1.0,
                    "date": "2020-11-05T08:13:28.537Z"
                  },
                  ...
                ],
  "wishlist": [
                {
                    "mid": a movie id,
                    "name": "name fo the movie",
                    "region": "movie's region",
                    "released_date": "date the movie released",
                    "average_rating": a rating number from 0 to 5, with one decimal digit,
                    "poster": "..."
                  },
                  {
                    "mid": 5,
                    "name": "Avengers: Age of Ultron",
                    "region": "United States",
                    "released_date": "2015-05-01T00:00:00Z",
                    "average_rating": 3.0,
                    "poster": "..."
                  },
                  ...
              ]
}
```
`"msg"` and `"success"` would contain following error message:
  1.  `{"success": false, "msg": "user did not log in", "profile_photo":"", "username":"", "top_reviews":[], "wishlist":[]}` indicates that the user didn't login to an account, which made the user fail to visit the user's own page.
  2.  `{"success": false, "msg": "target user does not exist", "profile_photo":"", "username":"", "top_reviews":[], "wishlist":[]}` indicates the user has already logged in, yet the username stored in session couldn't be found in database.
  3.  `{"success": false, "msg": "incorrect request method", "profile_photo":"", "username":"", "top_reviews":[], "wishlist":[]}` indicates method of the request is not `GET`.
  
Once successfully fetch needed information from database, ***`top_reviews` will contain the latest 5 reviews*** of the user (***may be less if the user has less than 5 reveiws***), and ***`wishlist` will contain 5 movies*** in the user's wishlist (***may be less if the user has less than 5 movies in wishlist***).

***:bangbang: Probs need movie posters in wishlist. Wishlist may need a date for every record so that can be sorted. :bangbang:***


<br/><br/>
### my_wishlist_view

**Author**: ZIJIAN SHEN

**Url**: http://127.0.0.1:8000/my_page/my_wishlist/

**Request Method**: GET

**Input Request**: No Input

**Output Data**:
```
{
  "success": true,
  "msg": "successfully get wishlist of the current user",
  "wishlist":[
                  {
                    "mid": 4,
                    "name": "The Avengers",
                    "region": "United States",
                    "released_date": "2012-05-04T12:00:00Z",
                    "average_rating": 3.8,
                    "poster": "..."
                  },
                  {
                    "mid": 5,
                    "name": "Avengers: Age of Ultron",
                    "region": "United States",
                    "released_date": "2015-05-01T00:00:00Z",
                    "average_rating": 3.0,
                    "poster": "..."
                  }
                ]
}
```
get all movies in wishlist of the current user.

1. `{"success": false, "msg": "user does not log in", "wishlist":[]}` indicates that user does not log in
2. `{"success": true, "msg": "successfully get wishlist of the current user", "wishlist":[...]}` means successfully get wishlist of the current user

***:bangbang: Probs need to sort movies. :bangbang:***
solved: sort the current user's wishlist by movie name

***:bangbang: Probs need movie posters in wishlist. Wishlist may need a date for every record so that can be sorted. :bangbang:***


<br/><br/>
### remove_from_wishlist_view

**Author**: ZIJIAN SHEN

**Url**: http://127.0.0.1:8000/my_page/my_wishlist/remove_from_wishlist/

**Request Method**: GET

**Input Request**:
```json
{
  "movie_id": "some movie id here, must be a positive integer"
}
```
**Output Data**:
```
{
  "success": true/false,
  "msg": "some message here"
}
```
remove movie given by movie_id from user's wish_list.

1. `{"success": false, "msg": "user does not log in"}` indicates that user does not log in
2. `{"success": false, "msg": "movie_id is required"}` means the input json dose not have movie_id field
3. `{"success": false, "msg": "movie_id must be a positive integer"}` indicates the input json does not follow the above input request
4. `{"success": false, "msg": "does not have movie with movie_id: " + str(movie_id)}` indicates the given movie_id field does not match any record in Movie database
5. `{"success": false, "msg": "movie with movie_id: " + str(movie_id) + " is not in wishlist"}` indicates the given movie is not in the user's wishlist
6. `{"success": true, "msg": "successfully remove movie from wishlist"}` indicates the given movie is successfully removed from the user's wishlist


<br/><br/>
### my_reviews_view

**Author**: ZIJIAN SHEN

**Url**: http://127.0.0.1:8000/my_page/my_reviews/

**Request Method**: GET

**Input Request**: No Input

**Output Data**: 
```
{
  "success": true,
  "msg": "successfully get reviewlist of the current user",
  "reviewlist":[
                  {
                    "user_id": 1,
                    "user_name": "pete@123.com",
                    "movie_id": 5,
                    "movie_name": "Avengers: Age of Ultron",
                    "review_comment": "some comment here, must be a string",
                    "rating_number": 1.0,
                    "date": "2020-11-05T10:20:09.849Z"
                  },
                  {
                    "user_id": 1,
                    "user_name": "pete@123.com",
                    "movie_id": 4,
                    "movie_name": "The Avengers",
                    "review_comment": "bad movie for movie_id = 4",
                    "rating_number": 1.0,
                    "date": "2020-11-05T08:13:28.537Z"
                  }
                ]
}
```
get all reviews left by the current user.
1. `{"success": false, "msg": "user does not log in", "reviewlist":[]}` indicates that user does not log in
2. `{"success": true, "msg": "successfully get reviewlist of the current user", "reviewlist":[...]}` indicates that successfully get reviewlist of the current user.


<br/><br/>
### get_review_view

**Author**: ZIJAIN SHEN

**Url**: http://127.0.0.1:8000/my_page/my_reviews/get_review/

**Request Method**: GET

**Input Request**:
```json
{
  "movie_id": "some movie id here, must be a positive integer"
}
```

**Output Data**:
```
{
  "success": true,
  "msg": "found review for movie_id: 5 left by the current user",
  "review":[
              {
                "user_id": 1,
                "user_name": "pete@123.com",
                "movie_id": 5,
                "movie_name": "Avengers: Age of Ultron",
                "review_comment": "some comment here, must be a string",
                "rating_number": 1.0,
                "date": "2020-11-05T10:20:09.849Z"
              }
            ]
}
```
get a single review left by the current user, for movie_id.

`"success"` indicates whether successfully get a single review left by the current user, for movie_id.

`"msg"` shows the current state.

1. `{"success": false, "msg": "user does not log in", "review": []}` indicates user does not log in
2. `{"success": false, "msg": "movie_id is required", "review": []}` indicates the input json dose not have movie_id field
3. `{"success": false, "msg": "movie_id must be a positive integer", "review": []}` indicates the input json does not follow the above input request
4. `{"success": false, "msg": "does not have movie with movie_id: " + str(movie_id), "review": []}` indicates the given movie_id field does not match any record in Movie database
5. `{"success": false, "msg": "the current user didn't leave a review for movie_id: " + str(movie_id), "review": []}` indicates there is no review left by the current user, for movie_id
6. `{"success": true, "msg": "found review for movie_id: " + str(movie_id) + " left by the current user", "review": [{...}]}` indicates found review that was left by the current user, for movie_id


<br/><br/>
### delete_review_view

**Author**: ZIJIAN SHEN

**Url**: http://127.0.0.1:8000/my_page/my_reviews/get_review/delete_review/

**Request Method**: GET

**Input Request**:
```json
{
  "movie_id": "some movie id here, must be a positive integer"
}
```
**Output Data**:
```
{
  "success": true/false,
  "msg": "some message here"
}
```
delete the review that was left by the current user, for movie_id

`"success"` indicates whether successfully delete the review left by the current user, for movie_id.

`"msg"` shows the current state.

1. `{"success": false, "msg": "user does not log in"}` indicates user does not log in
2. `{"success": false, "msg": "movie_id is required"}` indicates the input json dose not have movie_id field
3. `{"success": false, "msg": "movie_id must be a positive integer"}` indicates the input json does not follow the above input request
4. `{"success": false, "msg": "does not have movie with movie_id: " + str(movie_id)}` indicates the given movie_id field does not match any record in Movie database
5. `{"success": false, "msg": "the current user didn't leave a review for movie_id: " + str(movie_id)}` indicates there is no review left by the current user, for movie_id
6. `{"success": true, "msg": "successfully delete review"}` indicates successfully delete the review left by the current user, for movie_id


<br/><br/>
### edit_review_view
**Author**: ZIJIAN SHEN

**Url**: http://127.0.0.1:8000/my_page/my_reviews/get_review/edit_review/

**Request Method**: POST

**Input Request**:
```json
{
  "movie_id": "some movie id here, must be a positive integer",
  "review_comment": "some comment here, must be a string",
  "rating_number": "some rating number here, must be a positive number"
}
```
**Output Data**:
```
{
  "success": true/false
  "msg": "some message here",
}
```

edit the review that was left by the current user, for movie_id.

Note that only review_comment and rating_number are editable.

`"success"` indicates whether successfully edit review.

`"msg"` shows the current state.

1. `{"success": false, "msg": "user does not log in"}` indicates that user does not log in
2. `{"success": false, "msg": "movie_id, review_comment, rating_number are required"}` means the input json dose not have either movie_id field, or review_comment field, or rating_number field
3. `{"success": false, "msg": "movie_id must be a positive integer, review_comment must be a string, rating_number must be a positive number"}` indicates the input json does not follow the above input request
4. `{"success": false, "msg": "does not have movie with movie_id: " + str(movie_id)}` indicates the given movie_id field does not match any record in Movie database
5. `{"success": false, "msg": "the current user didn't leave a review for movie_id: " + str(movie_id)}` indicates there is no review left by the current user, for movie_id
6. `{"success": true, "msg": "successfully edit review"}` indicates successfully edit the review left by the current user, for movie_id


<br/><br/>
### my_bannedlist_view

**Author**: ZIJIAN SHEN

**Url**: http://127.0.0.1:8000/my_page/my_bannedlist/

**Request Method**: GET

**Input Request**: No Input

**Output Data**:
```
{
  "success": true,
  "msg": "successfully get blacklist of the current user",
  "bannedlist":[
                  {
                    "uid": 2,
                    "name": "holly@123.com",
                    "profile_photo": "..."
                  },
                  {
                    "uid": 6,
                    "name": "6@6.6",
                    "profile_photo": "..."
                  },
                  {
                    "uid": 7,
                    "name": "7@7.7",
                    "profile_photo": "..."
                  }
                ]
}
```
get all users in bannedlist of the current user.

1. `{"success": false, "msg": "user does not log in", "bannedlist":[]}` indicates that user does not log in
2. `{"success": true, "msg": "successfully get blacklist of the current user", "bannedlist":[...]}` indicates that successfully get blacklist of the current user.


<br/><br/>
### remove_from_bannedlist_view
**Author**: ZIJIAN SHEN

**Url**: http://127.0.0.1:8000/my_page/my_bannedlist/remove_from_bannedlist/

**Request Method**: GET

**Input Request**: 
```json
{
  "banned_user_id": "some banned_user_id, that you want to no longer block, must be a positive integer"
}
```
**Output Data**:
```
{
  "success": true/false,
  "msg": "some message here"
}
```

remove banned_user given by banned_user_id from user's blacklist.

1. `{"success": false, "msg": "user does not log in"}` indicates that user does not log in
2. `{"success": false, "msg": "banned_user_id is required"}` means the input json dose not have banned_user_id field
3. `{"success": false, "msg": "banned_user_id must be a positive integer"}` indicates the input json does not follow the above input request
4. `{"success": false, "msg": "does not have user with banned_user_id: " + str(banned_user_id)}` indicates the given banned_user_id field does not match any record in User database
5. `{"success": false, "msg": "user with banned_user_id: " + str(banned_user_id) + " is not in blacklist"}` indicates the given banned_user is not in the current user's blacklist
6. `{"success": true, "msg": "successfully remove user from blacklist"}` indicates the given banned_user is successfully removed from the current user's blacklist
<br/><br/>
<br/><br/>



## Other User's Page

### others_page_view

**Author**: PATRICK LI

**Url**: http://127.0.0.1:8000/user_page/

**Request Method**: GET

**Input Request**:
```
{
  "username": "a user name"
}
```
**Output Data**: 
```
{
  "success": true,
  "msg": "",
  "profile_photo": "a src path of target user's profile photo",
  "username" : "target user's username",
  "top_reviews":[
                  {
                    "user_id": a user id,
                    "user_name": "a username",
                    "movie_id": a movie id,
                    "movie_name": "the name of the movie",
                    "review_comment": "some comment here, must be a string",
                    "rating_number": a rating number from 0 to 5, with one decimal digit,
                    "date": "the date of review created/last edited"
                  },
                  {
                    "id": 1,
                    "user_id": 4,
                    "movie_id": 4,
                    "movie_name": "The Avengers",
                    "review_comment": "bad movie for movie_id = 4",
                    "rating_number": 1.0,
                    "date": "2020-11-05T08:13:28.537Z"
                  },
                  ...
                ],
  "wishlist": [
                {
                    "mid": a movie id,
                    "name": "name fo the movie",
                    "region": "movie's region",
                    "released_date": "date the movie released",
                    "average_rating": a rating number from 0 to 5, with one decimal digit,
                    "poster": "..."
                  },
                  {
                    "mid": 5,
                    "name": "Avengers: Age of Ultron",
                    "region": "United States",
                    "released_date": "2015-05-01T00:00:00Z",
                    "average_rating": 3.0,
                    "poster": "..."
                  },
                  ...
              ]
}
```
`"msg"` and `"success"` would contain following error message:
  1.  `{"success": false, "msg": "target user does not exist", "profile_photo":"", "username":"", "top_reviews":[], "wishlist":[]}` indicates the target username couldn't be found in database.
  2.  `{"success": false, "msg": "incorrect request method", "profile_photo":"", "username":"", "top_reviews":[], "wishlist":[]}` indicates method of the request is not `GET`.
  
Once successfully fetch needed information from database, ***`top_reviews` will contain the latest 5 reviews*** of the user (***may be less if the user has less than 5 reveiws***), and ***`wishlist` will contain 5 movies*** in the user's wishlist (***may be less if the user has less than 5 movies in wishlist***).

***:bangbang: Probs need movie posters in wishlist. Wishlist may need a date for every record so that can be sorted. :bangbang:***


<br/><br/>
### add_to_bannedlist_view

**Author**: ZIJIAN SHEN

**Url**: http://127.0.0.1:8000/user_page/add_to_bannedlist/

**Request Method**: GET

**Input Request**: 
```json
{
  "banned_user_id": "banned user, that you don't like, id here, must be a positive integer"
}
```

**Output Data**:
```
{
  "success": true/false
  "msg": "some message here",
}
```
add user, that the current user doesn't like, given by banned_user_id, to the current user's blacklist.

1. `{"success": false, "msg": "user does not log in"}` indicates that user does not log in
2. `{"success": false, "msg": "banned_user_id is required"}` means the input json dose not have banned_user_id field 
3. `{"success": false, "msg": "banned_user_id must be a positive integer"}` indicates the input json does not follow the above input request
4. `{"success": false, "msg": "does not have user with banned_user_id: " + str(banned_user_id)}` indicates that the user you want to add to your blacklist does not exist
5. `{"success": false, "msg": "user cannot add itself to its blacklist"}` indicates that user cannot add itself to its blacklist
6. `{"success": false, "msg": "banned_user_id: " + str(banned_user_id) + " already in blacklist"}` indicates that the user you want to block is already in your blacklist
7. `{"success": true, "msg": "successfully insert banned_user_id: " + str(banned_user_id) + " into blacklist"}` indicates that now the user with banned_user_id is in your blacklist


<br/><br/>
### others_wishlist_view

**Author**: PATRICK LI

**Url**: http://127.0.0.1:8000/user_page/user_wishlist/

**Request Method**: GET

**Input Request**: 
```
{
  "username": "a user name"
}
```
**Output Data**:
```
{
  "success": true,
  "msg": "successfully get wishlist of the target user",
  "wishlist":[
                  {
                    "mid": 4,
                    "name": "The Avengers",
                    "region": "United States",
                    "released_date": "2012-05-04T12:00:00Z",
                    "average_rating": 3.8,
                    "poster": "..."
                  },
                  {
                    "mid": 5,
                    "name": "Avengers: Age of Ultron",
                    "region": "United States",
                    "released_date": "2015-05-01T00:00:00Z",
                    "average_rating": 3.0,
                    "poster": "..."
                  },
                  ...
                ]
}
```

`"msg"` and `"success"` would contain following information:
  1. `{"success": true, "msg": "successfully get wishlist of the current user", "wishlist":[...]}` indicates successfully get wishlist of the target user.
  2.  `{"success": false, "msg": "does not have user [username]", "wishlist":[]}` indicates there's something with the target username.

***:bangbang: Probs need to sort movies. :bangbang:***

***:bangbang: Probs need movie posters in wishlist. Wishlist may need a date for every record so that can be sorted :bangbang:***
 

<br/><br/>
### others_reviews_view

**Author**: PATRICK LI

**Url**: http://127.0.0.1:8000/user_page/user_reviews/

**Request Method**: GET

**Input Request**: 
```
{
  "username": "a user name"
}
```
**Output Data**: 
```
{
  "success": true,
  "msg": "successfully get reviewlist of the current user",
  "reviewlist":[
                  {
                    "user_id": 1,
                    "user_name": "pete@123.com",
                    "movie_id": 5,
                    "movie_name": "Avengers: Age of Ultron",
                    "review_comment": "some comment here, must be a string",
                    "rating_number": 1.0,
                    "date": "2020-11-05T10:20:09.849Z"
                  },
                  {
                    "user_id": 1,
                    "user_name": "pete@123.com",
                    "movie_id": 4,
                    "movie_name": "The Avengers",
                    "review_comment": "bad movie for movie_id = 4",
                    "rating_number": 1.0,
                    "date": "2020-11-05T08:13:28.537Z"
                  },
                  ...
                ]
}
```
`"msg"` and `"success"` would contain following information:
  1.  `{"success": true, "msg": "successfully get reviewlist of the target user", "reviewlist":[...]}` indicates that successfully get reviewlist of the current user.
  2.  `{"success": false, "msg": "does not have user [username]", "wishlist":[]}` indicates there's something with the target username.
  
Once successfully fetch the review list from database, all reviews will be sorted by their created/last edited dates, from the latest to the earlist.

