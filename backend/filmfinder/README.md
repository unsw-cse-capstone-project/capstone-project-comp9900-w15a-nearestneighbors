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
### search_view
**Url**:  http://127.0.0.1:8000/search/

**Request Method**: GET

**Input Request**:
```json
{
  "keywords": "some key words here"
}
```
`"keywords"` is the keywords a user input to search for movies.

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


