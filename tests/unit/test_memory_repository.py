import pytest

from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory
from library.adapters.repository import RepositoryException


def test_repo_can_add_book(in_memory_repo):
    book = Book(12345, "test book")
    in_memory_repo.add_book(book)
    assert in_memory_repo.get_book(12345) is book


def test_repo_can_retrieve_book(in_memory_repo):
    book = in_memory_repo.get_book(25742454)
    assert book.title == "The Switchblade Mamma"
    assert in_memory_repo.get_book_price(book.book_id) == 0


def test_repo_can_get_all_books(in_memory_repo):
    books = in_memory_repo.get_all_books()
    assert len(books) == 20


def test_repo_can_add_user(in_memory_repo):
    user = User('username', 'Password1')
    in_memory_repo.add_user(user)
    assert in_memory_repo.get_user('username') is user


def test_repo_can_get_user(in_memory_repo):
    in_memory_repo.add_user(User('username', 'Password1'))
    user = in_memory_repo.get_user('username')
    assert user == User('username', 'Password1')


def test_repo_cannot_get_invalid_user(in_memory_repo):
    user = in_memory_repo.get_user('')
    assert user is None


def test_repo_can_add_review(in_memory_repo):
    book = in_memory_repo.get_book(25742454)
    review = Review(book, "test review", 5)
    in_memory_repo.add_review(review)
    assert review in in_memory_repo.get_reviews()


def test_repo_cannot_add_review_with_no_book(in_memory_repo):
    review = Review(None, "test review", 5)
    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repo_can_get_reviews(in_memory_repo):
    book = in_memory_repo.get_book(25742454)
    in_memory_repo.add_review(Review(book, "test", 1))
    in_memory_repo.add_review(Review(book, "test2", 2))
    assert len(in_memory_repo.get_reviews()) == 2


def test_repo_can_get_books_by_author_initial(in_memory_repo):
    books = in_memory_repo.get_books_by_author_initial('a')
    assert len(books) == 2


def test_repo_can_get_empty_list_when_getting_books_by_author_initial(in_memory_repo):
    books = in_memory_repo.get_books_by_author_initial('z')
    assert books == []


def test_repo_can_get_books_by_publisher_initial(in_memory_repo):
    books = in_memory_repo.get_books_by_publisher_initial('a')
    assert len(books) == 4


def test_repo_can_get_empty_list_when_getting_books_by_publisher_initial(in_memory_repo):
    books = in_memory_repo.get_books_by_publisher_initial('z')
    assert books == []


def test_repo_can_get_book_years(in_memory_repo):   # excludes None. years are sorted
    book_years = in_memory_repo.get_book_years()
    assert len(book_years) == 8
    assert book_years[0] == 1997
    assert book_years[1] == 2006
    for year in book_years:
        assert year is not None


def test_repo_can_get_books_with_no_year(in_memory_repo):
    books = in_memory_repo.get_books_with_no_year()
    assert len(books) == 4
    for book in books:
        assert book.release_year is None


def test_repo_can_get_books_by_year(in_memory_repo):
    books = in_memory_repo.get_books_by_year(2016)
    assert len(books) == 5
    assert books[0].title == "Cruelle"
    for book in books:
        assert book.release_year == 2016


def test_repo_can_get_empty_list_when_getting_books_by_year(in_memory_repo):
    books = in_memory_repo.get_books_by_year(-1)
    assert books == []


def test_repo_can_get_user_favourite_books(in_memory_repo):
    in_memory_repo.add_user(User('username', 'Password1'))
    # user = in_memory_repo.get_user('username')
    user_fav_books = in_memory_repo.get_user_favourite_books('username')
    assert user_fav_books == []
    in_memory_repo.add_book_to_user_favourites('username', 25742454)
    user_fav_books = in_memory_repo.get_user_favourite_books('username')
    assert str(user_fav_books) == '[<Book The Switchblade Mamma, book id = 25742454>]'


def test_repo_cannot_get_invalid_user_favourite_books(in_memory_repo):
    user_fav_books = in_memory_repo.get_user_favourite_books('invalid')
    assert user_fav_books is None


def test_repo_can_check_if_book_in_user_favourites(in_memory_repo):
    in_memory_repo.add_user(User('username', 'Password1'))
    in_memory_repo.add_book_to_user_favourites('username', 25742454)
    assert in_memory_repo.book_in_user_favourites('username', 25742454) is True
    assert in_memory_repo.book_in_user_favourites('username', -1) is False


def test_repo_cannot_check_if_book_in_invalid_user_favourites(in_memory_repo):
    assert in_memory_repo.book_in_user_favourites('username', 25742454) is None


def test_repo_can_add_to_user_favourites(in_memory_repo):
    in_memory_repo.add_user(User('username', 'Password1'))
    in_memory_repo.add_user(User('username2', 'Password2'))
    in_memory_repo.add_book_to_user_favourites('username', 25742454)
    assert in_memory_repo.book_in_user_favourites('username', 25742454) is True
    in_memory_repo.add_book_to_user_favourites('username2', 30128855)
    assert in_memory_repo.book_in_user_favourites('username2', 30128855) is True
    assert in_memory_repo.book_in_user_favourites('username2', 25742454) is False


def test_repo_can_remove_book_from_user_favourites(in_memory_repo):
    in_memory_repo.add_user(User('username', 'Password1'))
    in_memory_repo.add_book_to_user_favourites('username', 25742454)
    assert in_memory_repo.book_in_user_favourites('username', 25742454) is True
    in_memory_repo.remove_book_from_user_favourites('username', 25742454)
    assert in_memory_repo.book_in_user_favourites('username', 25742454) is False
