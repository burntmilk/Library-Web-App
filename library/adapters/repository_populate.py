from pathlib import Path
from library.adapters.repository import AbstractRepository
from library.adapters.jsondatareader import BooksJSONReader
from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory


def load_books(data_path: Path, repo: AbstractRepository, db_mode: bool):
    books_filename = str(Path(data_path) / "comic_books_excerpt.json")
    author_filename = str(Path(data_path) / "book_authors_excerpt.json")

    reader = BooksJSONReader(books_filename, author_filename)
    if not db_mode:     # memory
        # reader = BooksJSONReader(books_filename, author_filename)
        reader.read_json_files()
        books_list = reader.dataset_of_books

        for book in books_list:     # load the books into repo
            repo.add_book(book)

    else:   # database
        authors_json = reader.read_authors_file()
        books_json = reader.read_books_file()
        author_books = {}
        publisher_books = {}
        for book_json in books_json:

            book_id = book_json['book_id']
            authors = book_json['authors']
            publisher_name = book_json['publisher']
            for author in authors:
                author_id = author['author_id']
                if author_id not in author_books.keys():
                    author_books[author_id] = list()
                author_books[author_id].append(book_id)
            if publisher_name not in publisher_books.keys():
                publisher_books[publisher_name] = list()
            publisher_books[publisher_name].append(book_id)

            book_instance = Book(int(book_json['book_id']), book_json['title'])
            if book_json['publication_year'] != "":
                book_instance.release_year = int(book_json['publication_year'])
            if book_json['is_ebook'].lower() == 'false':
                book_instance.ebook = False
            else:
                if book_json['is_ebook'].lower() == 'true':
                    book_instance.ebook = True
            book_instance.description = book_json['description']
            if book_json['num_pages'] != "":
                book_instance.num_pages = int(book_json['num_pages'])

            repo.add_book(book_instance)

        for author_id in author_books.keys():
            numerical_id = int(author_id)
            author_name = None
            for author_json in authors_json:
                if int(author_json['author_id']) == numerical_id:
                    author_name = author_json['name']
            author = Author(numerical_id, author_name)
            for book_id in author_books[author_id]:
                book = repo.get_book(book_id)
                book.add_author(author)
            repo.add_author(author)

        for publisher_name in publisher_books.keys():
            publisher = Publisher(publisher_name)
            for book_id in publisher_books[publisher_name]:
                book = repo.get_book(book_id)
                book.publisher = publisher
            repo.add_publisher(publisher)




def load_users(data_path: Path, repo: AbstractRepository):
    pass


def load_reviews(data_path: Path, repo: AbstractRepository, users):
    pass


def populate(data_path: Path, repo: AbstractRepository, db_mode: bool):
    load_books(data_path, repo, db_mode)
