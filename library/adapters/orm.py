
from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import backref, mapper, relationship, synonym
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.sqltypes import Boolean, Float

from library.domain import model
from library.home.home import favourites

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('timestamp', DateTime, nullable=False),
    Column('review_text', String(280), nullable=True),
    Column('rating', Integer, nullable=False),
    Column('book_id', ForeignKey('books.id')),
    Column('user_id', ForeignKey('users.id'))
)

favourites_table = Table(
    'favourites', metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('book_id', ForeignKey('books.id'))
)

books_table = Table(
    'books', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('description', String(300), nullable=True),
    Column('release_year', Integer, nullable=True),
    Column('ebook', Boolean, nullable=True),
    Column('num_pages', Integer, nullable=True),
    Column('stock', Integer, nullable=True),
    Column('price', Float, nullable=True),
    Column('publisher_id', ForeignKey('publishers.id'))
)

authors_table = Table(
    'authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String, nullable=False)
)

book_authors_table = Table(
    'book_authors', metadata,
    Column('author_id', ForeignKey('authors.id')),
    Column('book_id', ForeignKey('books.id'))
)

publishers_table = Table(
    'publishers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False)
)

def map_model_to_tables():
    mapper(model.User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__favourite_books': relationship(model.Book),
        '_User__reviews': relationship(model.Review)
    })

    mapper(model.Review, reviews_table, properties={
        '_Review__book': relationship(model.Book),
        '_Review__review_text': reviews_table.c.review_text,
        '_Review__rating': reviews_table.c.rating,
        '_Review__timestamp': reviews_table.c.timestamp
    })

    mapper(model.Book, books_table, properties={
        '_Book__book_id': books_table.c.id,
        '_Book__title': books_table.c.title,
        '_Book__description': books_table.c.description,
        '_Book__publisher': relationship(model.Publisher, backref="_Publisher__name"),
        '_Book__authors':relationship(model.Author, secondary=book_authors_table),
        '_Book__release_year': books_table.c.release_year,
        '_Book__ebook': books_table.c.ebook,
        '_Book__num_pages': books_table.c.num_pages
    })

    mapper(model.Publisher, publishers_table, properties={
        '_Pubisher__name': publishers_table.c.name
    })

    mapper(model.Author, authors_table, properties={
        '_Author__unique_id':authors_table.c.id,
        '_Author__full_name':authors_table.c.full_name
    })