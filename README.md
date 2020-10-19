# Django library management system
[![Build Status](https://travis-ci.org/bihanviranga/librarysystem.svg?branch=master)](https://travis-ci.org/bihanviranga/librarysystem)

## Installation
- Create a virtual environment: `python -m virtualenv venv`
- Activate it: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Migrate the database: `python manage.py migrate`
- Load the sample data: `python manage.py loaddata sampledata.json`
- Run the server: `python manage.py runserver`
- Login to the default admin account with admin/admin

## Testing
- Run tests with `python manage.py test`
- Tests are tagged as general, book, book-instance, user, author.
- Run a specific group of tests with `python manage.py test --tag=general`

## Roadmap

### Todo
- [ ] Rename Rating.ratings to Rating.rating or something.
- [ ] For things like comments, forms, etc, can use sweetalert2.
- [ ] Check whether context['isAdmin'] is set in pages where it is necessary
- [ ] User profile management - change name, email, password.
- [ ] Trailing slash in URLConf for borrow and return causes error
- [ ] Testcases for not found views
- [ ] Read/not read marked in each book.
- [ ] Book instance types refactor into a seperate models (types can be hardcover, paperback, magazine, etc)
- [ ] User rate books.
- [ ] In books page, author is passed as a string (just the name). Cannot link to author page.

### Done
- [X] Author CRUD + Tests
- [X] Refactor tests into multiple files?
- [X] Book authors refactor into seperate models.
- [X] Borrowed/Available status on book instances
- [X] Borrow/Return functionality
- [X] Normal users who can view books and instances
- [X] Admin users who can CRUD books and instances
- [X] Admins can see a list of normal users.
- [X] Authentication features
- [X] BookInstance CRUD + Tests
- [X] Books CRUD + Tests
