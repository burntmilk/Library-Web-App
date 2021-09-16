from pathlib import Path
from typing import List     # for better documentation of function return types

from library.adapters.repository import AbstractRepository
from library.adapters.jsondatareader import BooksJSONReader
from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__books = []      # use BooksInventory class?
        self.__publishers = []
        self.__authors = []
        self.__users = []
        self.__reviews = []

    def add_book(self, book: Book):
        self.__books.append(book)

    def get_books(self) -> List[Book]:
        return self.__books

    def get_five_books(self, page_num: int) -> List[Book]:
        if page_num * 5 < len(self.__books):    # page numbers shouldn't go beyond list size
            return self.__books[(page_num-1) * 5: page_num * 5]
        else:
            return self.__books[(page_num-1) * 5: len(self.__books)]

    def get_book(self, book_id: int) -> Book:
        b = None
        for book in self.__books:
            if book.book_id == book_id:
                b = book
        return b



def load_books(data_path: Path, repo: MemoryRepository):    # makes list of book objects
    books_filename = str(Path(data_path) / "comic_books_excerpt.json")
    author_filename = str(Path(data_path) / "book_authors_excerpt.json")

    reader = BooksJSONReader(books_filename, author_filename)
    reader.read_json_files()
    books_list = reader.dataset_of_books

    for book in books_list:     # load the books into repo
        repo.add_book(book)


def load_users(data_path: Path, repo: MemoryRepository):
    pass


def load_reviews(data_path: Path, repo: MemoryRepository, users):
    pass


def populate(data_path: Path, repo: MemoryRepository):
    load_books(data_path, repo)
