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

`{ "success": true, "msg": None}` indicates the user successfully registerd a new account.


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
### search_by_name_view
**Url**:  http://127.0.0.1:8000/search_by_name/

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
              "rating": "latest averaged rating"
            },
              {
              "mid": "movie id", 
              "name": "movie name", 
              "released_date": "released year", 
              "poster": "src path of poster", 
              "rating": "latest averaged rating"
            },
              ...
          ]
}
```
`"success"` indicates whether the input keywords can conduct a search successfully.
`"result"` contains search result, which is a list of dictionaries. In each dictionary, there are `"mid"`, `"name"`, `"released_date"`, `"poster"`, and `"rating"`. 
They are used to demonstrate each movie in search result, except `"mid"`.
`{ "success": true, "result": []}` indicates no related movie is found.

### movie_list_view
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
              ]
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
              "cast":["test_actor1"]
            },

            ...

            {
              ...
            },

          ]
}
```
`"success"` indicates `http://127.0.0.1:8000/movies/` successfully return all movies.
`"result"` contains search result, which is a list of dictionaries. In each dictionary, there are `"mid"`, `"name"`, `"genre type"`, `"description"`,`"region"`,  `"released_date"`,`"director_name"`,`"poster"`,`"cast"` fields.

### detail_view
**Url**:  http://127.0.0.1:8000/movies/detail/

**Request Method**: GET
**Input Request**:
```json
{
  "movie_id": "input movie_id here (must be a integer)"
}
```

**Output Data**:
```
{
  "success": true,
  "msg": "found movie with movie_id: 1",
  "movie":[
            {
              "mid": 1,
              "name": "test_movie1",
              "genre":["test_genre1", "test_genre12", "test_genre3"],
              "description": "test_movie1_description",
              "region": "US",
              "released_date": "2020-10-30T09:37:52Z",
              "director": "test_director1",
              "poster": "../movies/posters/壁纸.jpg",
              "cast":["test_actor1", "test_actor2"]
            }
          ]
}
```
`"success"` indicates whether found matching movie.
`"msg"` shows the current state.
`"movie"` is a list, which has only one element, containing detail for the matching movie.
1. `{"success": false, "msg": "movie_id is required", "movie": []}` indicates there is no input in the GET Query Parameters.
2. `{"success": false, "msg": "movie_id must be a integer", "movie": []}` indicates the input is not a integer.
3. `{"success": false, "msg": "The movie you are looking for does not exist", "movie": []}` indicates there is no movie with mid == movie_id
4. `{"success": true, "msg": "found movie with movie_id", "movie": [{...}]}` indicates there is a movie with mid == movie_id
