from typing import List, Iterable
from library.adapters.repository import AbstractRepository
from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory


class NonExistentBookException(Exception):
    pass


class ReviewFormInvalid(Exception):
    pass


def get_book(book_id: int, repo: AbstractRepository) -> dict:
    book = repo.get_book(int(book_id))
    if book is None:
        raise NonExistentBookException
    return book_to_dict(book)


def get_all_books(repo: AbstractRepository) -> List[Book]:
    books = repo.get_books()
    books_dto = []
    if len(books) > 0:
        books_dto = books_to_dict(books)
    return books_dto


def get_book_stock(book_id: int, repo: AbstractRepository) -> int:
    stock = repo.get_book_stock(book_id)
    if stock is None:
        raise NonExistentBookException
    return stock


def get_book_price(book_id: int, repo: AbstractRepository) -> int:
    price = repo.get_book_price(book_id)
    if price is None:
        raise NonExistentBookException
    return price


def add_review(book_id: int, review_text: str, rating: int, repo: AbstractRepository):
    book = repo.get_book(book_id)
    if book is None:
        raise NonExistentBookException
    elif review_text is None or rating is None:
        raise ReviewFormInvalid

    review = Review(book, review_text, rating)
    repo.add_review(review)


def get_all_reviews_of_book(book_id: int, repo: AbstractRepository):
    reviews = repo.get_reviews()
    reviews_dto = []
    book = repo.get_book(book_id)
    if book is None:
        raise NonExistentBookException
    else:
        for review in reviews:
            if review.book == book:
                reviews_dto.append(review)
        return reviews_to_dict(reviews_dto)


# ============================================
# Functions to convert model entities to dicts. model / repo data -> primitive
# ============================================

def book_to_dict(book: Book):
    book_dict = {
        'book_id': book.book_id,
        'title': book.title,
        'description': book.description,
        'publisher': book.publisher.name,
        'authors': authors_to_dict(book.authors),
        'release_year': book.release_year,
        'ebook': book.ebook,
        'num_pages': book.num_pages
    }
    return book_dict


def books_to_dict(books: Iterable[Book]):  # returns list of books in dict format
    return [book_to_dict(book) for book in books]


def author_to_dict(author: Author):
    author_dict = {
        'author_id': author.unique_id,
        'full_name': author.full_name
    }
    return author_dict


def authors_to_dict(authors: Iterable[Author]):
    return [author_to_dict(author) for author in authors]


def review_to_dict(review: Review):
    review_dict = {
        'book': book_to_dict(review.book),
        'rating': review.rating,
        'review_text': review.review_text,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]