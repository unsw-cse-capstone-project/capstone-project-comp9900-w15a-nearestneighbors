# Django APIs

## Login
### login_view
Url: http://127.0.0.1:8000/login/

Request Method: POST

Input Request:
```json
{
  "name": "username",
  "password": "password"
}
```

Output Data:
```json
{
  "success": True,
  "msg": "This is login message"
}
```
"success" indicates whether the user successfully logged in or not.
"msg" contains error messages, which are:

1.```{ "success": False, "msg": "user already logged in"}``` indicates the user has already logged in.

2.```{ "success": False, "msg": "tuser doesn't exist"}``` indicates the input username doesn't exist in our database.

3.```{ "success": True, "msg": None}``` indicates the user logged in successfully.

4.```{ "success": False, "msg": "incorrect password"}``` indicates the user didn't input correct password.

5.```{ "success": False, "msg": "username and password are required"}``` indicates the user didn't input password and username.
  


