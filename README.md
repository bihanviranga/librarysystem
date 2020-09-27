# Django library management system

## Testing

- Run tests with `python manage.py test`
- Tests are tagged as general, book, book-instance, user.
- Run a specific group of tests with `python manage.py test --tag=general`

## Roadmap

### Todo
- [ ] (ONGOING) Book authors refactor into seperate models.
- [ ] (ONGOING) Because author was refactored, check every page where author is displayed. (books, book details)
- [ ] Testcases for not found views
- [ ] Read/not read marked in each book.
- [ ] Book instance types refactor into a seperate models (types can be hardcover, paperback, magazine, etc)
- [ ] User rate books.

### Done
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
- [X] Edit instance types
- [X] Remove book instances
- [X] View specific book instance.
- [X] Add book instances
- [X] View list of book instances in book detail page.
- [X] Edit book details.
- [X] Delete books.
- [X] View book details.
- [X] Add new books.
- [X] Look into class-based views.
- [X] Display a list of books.
