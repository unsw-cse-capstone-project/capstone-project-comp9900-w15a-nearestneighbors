# capstone-project-comp9900-w15a-nearestneighbors
## work diary
work diary directory contains each team member's work diary, using zID to name them (e.g. z5224890.txt), team members should update this file every week.

## Django Setup
1.  Clone this repo and go to the directory backend/filmfinder in terminal

2.  Check and copy the path of python3 installed on your machine by
        ```
        $ which python3
        ```
      
2.  Create a virtual environment for the project by entering
        ```
        $ virtualenv your_venv ip (paste your python3 path here)
        ```
      
4.  Activate your virtual environment by:
        ```
        $ source bin/activate
        ```
    You can deactivate your virtual environment by
        ```
        (your_env)$ deactivate
        ```
        
5.  Install Django in your activated virtual environment by: 
        ```
        (your_env)$ pip install django
        ```
        
6.  Install Django Rest Framework in your activated virtual environment by: 
        ```
        (your_env)$ pip install djangorestframework
        ```
        
5.  Now you can run the server by: 
        ```
        (your_env)$ python3 manage.py runserver
        ```
