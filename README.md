# imagersite

**Authors**: 
- Keith Eckert [Git Hub](https://github.com/keitheck) | [Linkedin](www.linkedin.com/in/keith-eckert)
- David Snowberger [Git Hub](https://github.com/dsnowb) | [Linkedin](www.linkedin.com/in/dsnowberger)

**Version**: 0.1.0

## Overview
An image bucket app.

## Architecture
This app is written using Python 3.6, Django, and Postgres, HTML, CSS

## Installation

1. Clone https://github.com/keitheck/django-imager

2. pip install -r requirments.txt

3. create postgres db

4. set up local environmental variables in your environment

```
# Project-specific env variables
export SECRET_KEY='<your secret key>'
export DB_NAME='<db name>'
export DB_USER=''
export DB_PASSWORD=''
export DB_HOST='localhost'
```

5. In project directory run:

`./manage.py runserver` The server should now be running on localhost:8000

## Routes

### /admin/

- admin login page

### /

- home page

### /profile/

- user profile page

### /accounts/

- user authentication and registration

### /images/photos

- gallery of all uploaded public photos

### /images/photos/<photo_id>

- individual photo

### /images/albums

- gallery of all uploaded public albums

### /images/albums/<album_id>

- individual album

### /images/library

- user's personal library

## Change Log
| Date | |
|:--|:--|
| 23 April 2018 | Repo Created, initial setup, profile model configured. Tested |
| 24 April 2018 | Configured Authentication, CSS, Tested |
| 25 April 2018 | Configured Album and Photo models. Tested |
| 26 April 2018 | Added library, photo and album routes. Tested |

## Resources
- Django
- Amazon AWS
