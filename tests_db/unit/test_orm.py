import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from library.domain.model import User, Book, Review, Author, Publisher


def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_book(empty_session):
    empty_session.execute(
        'INSERT INTO books (id, title, description, release_year, ebook, num_pages) VALUES '
        '(707611, "Superman Archives, Vol. 2", "test description", 1997, False, 272)'
    )
    row = empty_session.execute('SELECT id FROM books').fetchone()
    return row[0]


def insert_author(empty_session):
    empty_session.execute(
        'INSERT INTO authors (id, full_name) VALUES (81563, "Jerry Siegel"), (89537, "Joe Shuster")'
    )
    rows = list(empty_session.execute('SELECT id FROM authors'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_publisher(empty_session):
    empty_session.execute(
        'INSERT INTO publishers (name) VALUES ("DC Comics")'
    )
    row = empty_session.execute('SELECT id FROM publishers').fetchone()
    return row[0]


def insert_author_book_associations(empty_session, book_key, author_keys):
    stmt = 'INSERT INTO book_authors (author_id, book_id) VALUES (:author_id, :book_id)'
    for author_key in author_keys:
        empty_session.execute(stmt, {'author_id': author_key, 'book_id': book_key})


def insert_publisher_book_associations(empty_session, book_key, publisher_key):
    stmt = 'UPDATE books (publisher_id) VALUES (:publisher_id) WHERE (id == :book_id)'
    empty_session.execute(stmt, {'publisher_id': publisher_key, 'book_id': book_key})


def make_book():
    book = Book(707611, "Superman Archives, Vol. 2")
    book.description = "test description"
    book.release_year = 1997
    book.ebook = False
    book.num_pages = 272
    return book


def make_user():
    user = User('Andrew', '1234')
    return user


def make_author():
    author = Author(81563, "Jerry Siegel")
    return author