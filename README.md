Library Project
======

Description
----------------------
LibraryProject is an app that will allow you to keep track of who is borrowing your books.  Simply search for a book (using a Goodreads api), select who you are and who you're borrowing it from, and enter your new loan into our system.


Developer Installation
----------------------

0. Ensure that Python 3 is installed on your machine (https://www.python.org/downloads/)

1. Create a directory for development projects on your machine

        $ mkdir /<path on your machine>/projects
        $ cd /<path>/projects

2. Clone the repository

        $ git clone <library project address>
        $ cd libraryproject

3. Create a virtual environment and activate it

        $ pyvenv ENV
        $ source ENV/bin/activate

4. Install dependencies to the virtual environment

        (ENV)$ pip install -r requirements.txt
        
4.5 Migrate models if necessary

        (ENV)$ cd libraryproject
        (ENV)$ python manage.py makemigrations
        (ENV)$ python manage.py migrate
  
5. Load test data

        (ENV)$ python manage.py loaddata users
        (ENV)$ python manage.py loaddata data
        
Other Instructions
----------------------

We are in developer mode at the moment, so please feel free to use the following login information for testing on your local machine:  login:admin and password:adminis289. 
