from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory
from library.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_book(self, book: Book):
        with self._session_cm as scm:
            # print(book)     # test
            scm.session.add(book)
            scm.commit()

    def get_all_books(self) -> List[Book]:  # possibly change, as books will always be in db
        books = []
        try:
            books = self._session_cm.session.query(Book).all()
        except NoResultFound:
            pass
        return books

    def get_book(self, book_id: int) -> Book:
        book = None
        try:
            book = self._session_cm.session.query(Book).filter(Book._Book__book_id == book_id).one()
        except NoResultFound:
            pass
        return book

    def get_book_stock(self, book_id: int) -> int:
        # return 0
        stock = self._session_cm.session.execute('SELECT stock FROM books WHERE id = :book_id',
                                               {'book_id': book_id}).fetchone()
        if stock:
            return stock
        return 0

    def get_book_price(self, book_id: int) -> int:
        # return 0
        price = self._session_cm.session.execute('SELECT price FROM books WHERE id = :book_id',
                                               {'book_id': book_id}).fetchone()
        if price:
            return price
        return 0

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            pass
        return user

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user_favourite_books(self, user_name: str) -> List[Book]:
        user = self.get_user(user_name)
        if user:    # not none
            return user.favourite_books
        pass

    def book_in_user_favourites(self, user_name: str, book_id: int) -> bool:
        pass

    def add_book_to_user_favourites(self, user_name: str, book_id: int):
        pass

    def remove_book_from_user_favourites(self, user_name, book_id: int):
        pass

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_reviews(self) -> List[Review]:
        reviews = []
        try:
            reviews = self._session_cm.session.query(Review).all()
        except NoResultFound:
            pass
        return reviews

    def get_books_by_author_initial(self, initial_letter: str) -> List[Book]:
        books = []
        author_ids = self._session_cm.session.execute(
            'SELECT id FROM authors WHERE SUBSTRING(full_name, 1, 1) = :initial',
             {'initial': initial_letter.upper()}).all()
        if author_ids:
            book_ids = []
            for author_id in author_ids:
                author_id = int(author_id[0])
                book_ids += (self._session_cm.session.execute(
                    'SELECT book_id FROM book_authors WHERE author_id = :author_id',
                    {'author_id': author_id}).all())[0]
            books = self._session_cm.session.query(Book).filter(Book._Book__book_id.in_(book_ids)).all()
        return books

    def get_books_by_publisher_initial(self, initial_letter: str) -> List[Book]:
        books = []
        publisher_ids = self._session_cm.session.execute(
            'SELECT id FROM publishers WHERE SUBSTRING(name, 1, 1) = :initial',
            {'initial': initial_letter.upper()}).all()
        print(publisher_ids)
        if publisher_ids:
            book_ids = []
            for publisher_id in publisher_ids:
                publisher_id = int(publisher_id[0])
                book_ids += (self._session_cm.session.execute(
                    'SELECT id FROM books WHERE publisher_id = :publisher_id',
                    {'publisher_id': publisher_id}).all())
                book_ids = [id[0] for id in book_ids]
            books = self._session_cm.session.query(Book).filter(Book._Book__book_id.in_(book_ids)).all()
        return books

    def get_book_years(self) -> List[int]:
        years = []
        try:
            years = self._session_cm.session.execute(
                'SELECT DISTINCT release_year FROM books WHERE release_year IS NOT NULL').all()
            years = [year[0] for year in years]
        except NoResultFound:
            pass
        return years

    def get_books_with_no_year(self) -> List[Book]:
        books = []
        try:
            books = self._session_cm.session.query(Book).filter(Book._Book__release_year == None)
        except NoResultFound:
            pass
        return books

    def get_books_by_year(self, year: int) -> List[Book]:
        books = []
        try:
            books = self._session_cm.session.query(Book).filter(Book._Book__release_year == year)
        except NoResultFound:
            pass
        return books

    def add_author(self, author: Author):
        with self._session_cm as scm:
            scm.session.add(author)
            scm.commit()

    def add_publisher(self, publisher: Publisher):
        with self._session_cm as scm:
            scm.session.add(publisher)
            scm.commit()
