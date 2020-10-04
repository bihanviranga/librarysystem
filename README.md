# Django library management system

## Testing

- Run tests with `python manage.py test`
- Tests are tagged as general, book, book-instance, user, author.
- Run a specific group of tests with `python manage.py test --tag=general`

## Roadmap

### Todo
- [ ] Tests for DELETE, UPDATE
- [ ] Tests - POST request send as both admin and normal user?
- [ ] Author CRUD (Done so far: Create, Retrieve)
- [ ] Trailing slash in URLConf for borrow and return causes error
- [ ] Testcases for not found views
- [ ] Read/not read marked in each book.
- [ ] Book instance types refactor into a seperate models (types can be hardcover, paperback, magazine, etc)
- [ ] User rate books.

### Done
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
