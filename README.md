# capstone-project-comp9900-w15a-nearestneighbors
## Work Diary
work diary directory contains each team member's work diary, using zID to name them (e.g. z5224890.txt), team members should update this file every week.

## Django Setup
1.  Clone this repo and go to the directory `backend/filmfinder` in terminal.
2.  Check and copy the path of python3 installed on your machine by
```
        $ which python3
```
3.  Create a virtual environment for the project by entering
```
        $ virtualenv your_venv -p (paste your python3 path here)
```
4.  Activate your virtual environment by
```
        $ source bin/activate
```
   You can deactivate your virtual environment by
```
        (your_venv)$ deactivate
```
5.  Install Django in your activated virtual environment by
```
        (your_venv)$ pip install django
```
6.  Install Django Rest Framework in your activated virtual environment by
```
        (your_venv)$ pip install djangorestframework
```
7.  Install packages needed in your activated virtual environment by: 
```
        (your_venv)$ pip install Pillow
        (your_venv)$ pip install simplejson
        (your_venv)$ pip install django-extensions
        (your_venv)$ pip install pandas
        (your_venv)$ pip install -U scikit-learn
        (your_venv)$ pip install numpy==1.19.2
        (your_venv)$ pip install django-pandas
        (your_venv)$ pip install rake-nltk
        (your_venv)$ pip install funkybob
```
8.  Now you can run the server by 
```
        (your_venv)$ python3 manage.py runserver
```
   If port 8000 (by default) is in user, you can use other port by
```
        (your_venv)$ python3 manage.py runserver (port number)
```
        
<br></br>
**On CSE machine**:

1.  Clone this repo to your CSE machine and go to the directory `backend/filmfinder` in terminal.
2.  Create a virtual environment for the project by entering
```
        $ python3 -m venv your_venv
```
3.  Follow the step 4 to 8 above to set up Django.


</br></br>
## Frontend Setup
1.  Clone this repo to your CSE machine and go to the directory ../frontend in terminal.
2.  Install all of the dependencies needed to run the ReactJS app
```
        $ yarn
```
3.  Start the ReactJS app, it will automatically open your browser and load the homepage of our film finder
```
        $ yarn start
```
4.  If you changed the port number in Django setup, please go to `../frontend/package.json` , replace the port number 8000 in line 2 with the port number you chose. For example, I chose port 8001, then line 2 will be
```
        “proxy”: “http://localhost:8001”,
```


<br></br>
**On CSE machine**:
1.  Clone this repo to your CSE machine and go to the directory ../frontend in terminal.
2.  Install all of the dependencies needed to run the ReactJS app
```
        $ npm install
```
3.  Start the ReactJS app, it will automatically open your browser and load the homepage of our film finder
```
        $ npm start
```
4.  Follow the step 4 above.
