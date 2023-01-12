Django 3.0 supports Python 3.6, 3.7, and 3.8. 
Using a virtual environment is highly recommended although not strictly required.

$ cd src/for_django_3-0
$ pip install -r requirements.txt (only if you don't have Django 3.0 installed)
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver 0.0.0.0:9898
