# Django APIs

## Login

### index_view
**Url**:  http://127.0.0.1:8000/index/

**Request Method**: GET

**Input Request**:  N/A

**Output Data**:
```json
{
  "login_flag": true,
  "name": "username"
}
```
`"login_flag"` indicates whether a user has logged in. 
If so, `"name"` will be the username. 
If not, `"name"` will be `None`.


<br/><br/>
### login_view
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
  "msg": "This is login message"
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
`"msg"` contains error messages if `"success"` is `false`, which are:
  1. `{ "success": false, "msg": "user didn't log in"}` indicates the user didn't logged in with an existing account.

`{ "success": true, "msg": None}` indicates the user successfully logged out, and the session has been flushed.
<br/><br/>
<br/><br/>

## Movies
### search_view
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
`"success"` indicates `http://127.0.0.1:8000/movies/` successfully return all movies.

`"movies"` contains search result, which is a list of dictionaries. 

In each dictionary, there are `"mid"`, `"name"`, `"genre type"`,`"description"`,`"region"`,  `"released_date"`,`"director_name"`,`"poster"`,`"cast"`,`"average_rating"` fields.

Note that if the user is logged in, the `"average_rating"` field will exclude reviews given by users in banned list.

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
  ]
}
```
`"success"` indicates whether found matching movie.

`"msg"` shows the current state.

`"movie"` is a list, which has only one element, containing detail for the matching movie.

1. `{"success": false, "msg": "movie_id is required", "movie": []}` indicates there is no input in the GET Query Parameters.
2. `{"success": false, "msg": "movie_id must be a positive integer", "movie": []}` indicates the input is not a positive integer.
3. `{"success": false, "msg": "does not have movie with movie_id: " + "str(movie_id)", "movie": []}` indicates there is no movie with mid == movie_id
4. `{"success": true, "msg": "found movie with movie_id: " + "str(movie_id)", "movie": [{...}]}` indicates there is a movie with mid == movie_id

Note that if the user is logged in, the `"reviews"` field will exclude reviews given by users in banned list.

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
1. `{"success": false, "msg": "user does not log in"}` indicates that user does not log in
2. `{"success": false, "msg": "movie_id is required"}` means the input json dose not have movie_id field
3. `{"success": false, "msg": "movie_id must be a positive integer"}` indicates the input json does not follow the above input request
4. `{"success": false, "msg": "does not have movie with movie_id: " + "str(movie_id)"}` indicates the given movie_id field does not match any record in Movie database
5. `{"success": false, "msg": "movie already in wishlist"}` indicates the given movie is already in wishlist
6. `{"success": true, "msg": "successfully insert movie to wishlist"}` indicates the given movie is successfully inserted into wishlist


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
`"success"` indicates whether successfully return all reviews.

`"msg"` shows the current state.

1. `{"success": false, "msg": "movie_id is required", "reviews": []}` indicates there is no input in the GET Query Parameters.
2. `{"success": false, "msg": "movie_id must be a positive integer", "reviews": []}` indicates the input is not a positive integer.
3. `{"success": false, "msg": "does not have movie with movie_id: " + "str(movie_id)", "reviews": []}` indicates there is no movie with mid == movie_id
4. `{"success": true, "msg": "found all reviews for movie_id: " + "str(movie_id)", "reviews": [{...}, {...}]}` indicates there is a movie with mid == movie_id, and found all reviews for this movie.

Note that if the user is logged in, the `"reviews"` field will exclude reviews given by users in banned list.



### new_review_view
**Author**: ZIJIAN SHEN

**Url**:  http://127.0.0.1:8000/movies/detail/new_review/

**Request Method**: POST

**Input Request**:
```json
{
  "movie_id": "some movie id here, must be a positive integer", 
  "review_comment": "some comment here, must be a string",
  "rating_number": "some rating number here, must be a positive number",
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
3. `{"success": false, "msg": "movie_id must be a positive integer, review_comment must be a string,rating_number must be a positive number"}` indicates the input json does not follow the above input request
4. `{"success": false, "msg": "does not have movie with movie_id: " + "str(movie_id)"}` indicates the given movie_id field does not match any record in Movie database
5. `{"success": false, "msg": "each user can only leave one review for a movie, but reviews are editable"}` indicates that there is already a review for the current user and the given movie
6. `{"success": true, "msg": "successfully create a new review"}` indicates a new review is created

