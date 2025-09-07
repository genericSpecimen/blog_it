# blog_it
A blogging platform made with Django.

[![BlogIt CI/CD](https://github.com/genericSpecimen/blog_it/actions/workflows/blogit-CI-CD.yml/badge.svg)](https://github.com/genericSpecimen/blog_it/actions/workflows/blogit-CI-CD.yml)
![Coverage](https://raw.githubusercontent.com/genericSpecimen/blog_it/main/coverage.svg)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Check it out [here](https://blog-it-xigs.onrender.com/blog/)!

## Features

* User Sign Up / Log in / Log out
* Editable account / profile information
* Assignable categories to blog posts, e.g., Science, Nature, etc
* Filterable blog posts on the basis of categories
* Users can comment on blog posts
* Users can follow each other, and have their own personalized "feed"

## Run it yourself


```bash
# clone the repo
git clone https://github.com/genericSpecimen/blog_it.git

cd blog_it/

# create a vitual environment, install dependencies, run migrations, run the server
make start
```

At this point, the development server should start at [http://127.0.0.1:8000/](http://127.0.0.1:8000/). But there is no data in the database. We also need to create a superuser.

```bash
source env/bin/activate

# create superuser
python manage.py createsuperuser

# run the server again
make run
```

Go to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and log in with the superuser credentials. You can now either use the admin dashboard to create objects or simply use the user Sign Up / Log In features on the website.

## Made with

* [Django](https://www.djangoproject.com/)
* [Bootstrap 4](https://getbootstrap.com/)

## To Do
- [x] Create a To Do list.
- [x] Create the skeleton project.
- [x] Create models for BlogAuthor, BlogPost, BlogComment.
- [x] Register the models and add test objects using the admin site.
- [x] Customize the admin site.
- [x] Create the home page.
- [x] Create BlogPost and BlogAuthor list and detail views.
- [x] Add user log in / log out functionality.
- [x] Add the functionality of commenting on blog posts.
- [x] Write basic tests
- [x] Improve the user interface a bit
- [x] Allow users to create their own accounts with profile information.
- [x] Allow users to create their own blog posts
- [x] Add a blog post category feature.
- [x] Add a blogger subscribe feature.
