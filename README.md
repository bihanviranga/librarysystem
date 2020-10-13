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
- [ ] Author CRUD (Done so far: Create, Retrieve)
- [ ] Check whether context['isAdmin'] is set in pages where it is necessary
- [ ] Trailing slash in URLConf for borrow and return causes error
- [ ] Testcases for not found views
- [ ] Read/not read marked in each book.
- [ ] Book instance types refactor into a seperate models (types can be hardcover, paperback, magazine, etc)
- [ ] User rate books.
- [ ] Users can change passwords.
- [ ] In books page, author is passed as a string (just the name). Cannot link to author page.

### Done
- [X] Tests for DELETE, UPDATE
- [X] Tests - POST request send as both admin and normal user?
- [X] Since control tests are making it large, refactor tests into multiple files?
- [X] Author page to show information and books
- [X] Because author was refactored, check every page where author is displayed. (books, book details)
- [X] Book authors refactor into seperate models.
- [X] Since Books is not a list view anymore, test it!
- [X] Borrowed/Available status on book instances
- [X] Borrow/Return functionality
- [X] Normal users who can view books and instances
- [X] Admin users who can CRUD books and instances
- [X] Admins can see a list of normal users.
- [X] Authentication features
- [X] BookInstance CRUD
- [X] Books CRUD
