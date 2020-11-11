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
        (your_venv)$ pip install numpy
        (your_venv)$ pip install django-pandas
        (your_venv)$ pip install rake-nltk
        (your_venv)$ pip install funkybob
```
8.  Now you can run the server by 
```
        (your_venv)$ python3 manage.py runserver
```
        
<br></br>
**On CSE machine**:

1.  Clone this repo to your CSE machine and go to the directory `backend/filmfinder` in terminal.
2.  Create a virtual environment for the project by entering
```
        $ python3 -m venv your_venv
```
3.  Follow the step 4 to 8 above to set up Django.
