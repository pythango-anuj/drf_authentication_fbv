# DRF Authentication System Using Function based View
Django REST framework is a powerful and flexible toolkit for building Web APIs. In this project we are 
mainly focussing Authentication APIS.

There are many ways to develop Authenticating apis in DRF but in this project we have designed our own custom user model
and used Function based implementation of views to write view code. In our case 
we have written codes for three main operations of authentication and one more view for listing all users:

1). Register(Add a new User)

2). Login

3). Logout

4). List of all Users(Only for Admin users)


Apart from that one another tool that we have used in this project is [drf_yasg(Swagger Generator)](https://drf-yasg.readthedocs.io/en/stable/readme.html) 
for API Documentation which makes our API look awesome.

# PREQUISITES

Following programmes should be installed on your computer to run this project properly:

Python 3.6+

Virtual Environment

To install virtual environment on your system use:

pip install virtualenv

# Installation and Running :

git clone https://github.com/pythango/drf_authentication_fbv.git

virtualenv myenv

source myenv/bin/activate

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

Open Browser and Type http://127.0.0.1:8000