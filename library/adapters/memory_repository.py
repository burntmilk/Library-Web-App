import json
from pathlib import Path

from library.adapters.jsondatareader import BooksJSONReader
from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory


class MemoryRepository():
    pass


def load_books(data_path: Path, repo: MemoryRepository):
    pass


def load_users(data_path: Path, repo: MemoryRepository):
    pass


def load_reviews(data_path: Path, repo: MemoryRepository, users):
    pass


def populate(data_path: Path, repo: MemoryRepository):
    pass
