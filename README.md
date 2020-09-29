# Django library management system

## Testing

- Run tests with `python manage.py test`
- Tests are tagged as general, book, book-instance, user.
- Run a specific group of tests with `python manage.py test --tag=general`

## Roadmap

### Todo
- [ ] Since control tests are making it large, refactor tests into multiple files?
- [ ] Tests for DELETE, UPDATE
- [ ] Tests - POST request send as both admin and normal user?
- [ ] Author CRUD (Done so far: Create, Retrieve)
- [ ] Trailing slash in URLConf for borrow and return causes error
- [ ] Testcases for not found views
- [ ] Read/not read marked in each book.
- [ ] Book instance types refactor into a seperate models (types can be hardcover, paperback, magazine, etc)
- [ ] User rate books.

### Done
- [X] Author page to show information and books
- [X] Because author was refactored, check every page where author is displayed. (books, book details)
- [X] Book authors refactor into seperate models.
- [X] Instance list views shows borrowed/not borrowed.
- [X] Since Books is not a list view anymore, test it!
- [X] Book list view shows how many available or not.
- [X] Normal users cannot mark books as borrowed.
- [X] Admins can mark books as borrowed/returned.
- [X] Users can see the books they have borrowed.
- [X] Admins can see who borrowed books.
- [X] Normal users can see whether a book is borrowed or not.
- [X] All users can borrow books.
- [X] Users can return borrowed books.
- [X] Normal users who can view books and instances
- [X] Admin users who can CRUD books and instances
- [X] Admins can see a list of normal users.
- [X] Authentication features
- [X] BookInstance CRUD
- [X] Books CRUD
