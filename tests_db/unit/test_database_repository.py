from datetime import date, datetime

import pytest

import library.adapters.repository as repo
from library.adapters.database_repository import SqlAlchemyRepository
from sqlalchemy import exc
from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory
from library.adapters.repository import RepositoryException


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('Dave', 'Password1')
    repo.add_user(user)
    repo.add_user(User('Martin', 'Password1'))
    user2 = repo.get_user('dave')
    print(user2)
    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user(User('Martin', 'Password1'))
    user = repo.get_user('martin')
    assert user == User('Martin', 'Password1')


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('prince')
    assert user is None


def test_repository_can_add_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = Book(1, 'test')
    repo.add_book(book)
    assert repo.get_book(1) == book


def test_repository_can_retrieve_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = repo.get_book(707611)
    assert book.title == 'Superman Archives, Vol. 2'


def test_repository_can_not_retrieve_a_non_existent_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = repo.get_book(-1)
    assert book is None


def test_repository_can_get_all_books(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    books = repo.get_all_books()
    assert len(books) == 20
    assert type(books[0]) is Book


def test_repository_can_get_stock(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    stock = repo.get_book_stock(707611)
    assert stock == 0


def test_repository_can_get_price(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    price = repo.get_book_price(707611)
    assert price == 0


def test_repo_can_add_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = repo.get_book(707611)
    review = Review(book, 'test review', 5)
    repo.add_review(review)
    assert review in repo.get_reviews()


def test_repo_cannot_add_review_with_no_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    review = Review(None, 'test review', 5)
    with pytest.raises(RepositoryException):
        repo.add_review(review)


def test_repo_can_get_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = repo.get_book(707611)
    assert len(repo.get_reviews()) == 0
    review = Review(book, 'test review', 5)
    repo.add_review(review)
    assert len(repo.get_reviews()) == 1


def test_repo_can_get_books_by_author_initial(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    books = repo.get_books_by_author_initial('a')
    assert len(books) == 2


def test_repo_can_get_empty_list_when_getting_books_by_author_initial(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    books = repo.get_books_by_author_initial('z')
    assert books == []


def test_repo_can_get_books_by_publisher_initial(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    books = repo.get_books_by_publisher_initial('a')
    assert len(books) == 4


def test_repo_can_get_empty_list_when_getting_books_by_publisher_initial(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    books = repo.get_books_by_publisher_initial('z')
    assert books == []


def test_repo_can_get_book_years(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book_years = repo.get_book_years()
    assert len(book_years) == 8
    assert book_years[0] == 1997
    assert book_years[1] == 2006
    for year in book_years:
        assert year is not None


def test_repo_can_get_books_with_no_year(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    books = repo.get_books_with_no_year()
    for book in books:
        assert book.release_year is None


def test_repo_can_get_books_by_year(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    books = repo.get_books_by_year(2016)
    for book in books:
        assert book.release_year == 2016


def test_repo_can_get_user_favourite_books(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user(User('username', 'Password1'))
    user_fav_books = repo.get_user_favourite_books('username')
    assert user_fav_books == []
    repo.add_book_to_user_favourites('username', 25742454)
    user_fav_books = repo.get_user_favourite_books('username')
    assert str(user_fav_books) == '[<Book The Switchblade Mamma, book id = 25742454>]'


def test_repo_cannot_get_invalid_user_favourite_books(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    with pytest.raises(TypeError):
        user_fav_books = repo.get_user_favourite_books('invalid')


def test_repo_can_check_if_book_in_user_favourites(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user(User('username', 'Password1'))
    repo.add_book_to_user_favourites('username', 25742454)
    assert repo.book_in_user_favourites('username', 25742454) is True


def test_repo_cannot_check_if_book_in_invalid_user_favourites(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    with pytest.raises(exc.NoResultFound):
        in_user_favs = repo.book_in_user_favourites('username', 25742454) is None


def test_repo_cannot_check_if_invalid_book_in_user_favourites(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user(User('username', 'Password1'))
    with pytest.raises(exc.NoResultFound):
        in_user_favs = repo.book_in_user_favourites('username', -1) is None


def test_repo_can_add_to_user_favourites(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user(User('username', 'Password1'))
    repo.add_user(User('username2', 'Password2'))
    repo.add_book_to_user_favourites('username', 25742454)
    assert repo.book_in_user_favourites('username', 25742454) is True
    repo.add_book_to_user_favourites('username2', 30128855)
    assert repo.book_in_user_favourites('username2', 30128855) is True
    assert repo.book_in_user_favourites('username2', 25742454) is False


def test_repo_can_remove_book_from_user_favourites(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user(User('username', 'Password1'))
    repo.add_book_to_user_favourites('username', 25742454)
    assert repo.book_in_user_favourites('username', 25742454) is True
    repo.remove_book_from_user_favourites('username', 25742454)
    assert repo.book_in_user_favourites('username', 25742454) is False
