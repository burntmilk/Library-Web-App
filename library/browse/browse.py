from flask import Blueprint, render_template
from library.adapters.jsondatareader import BooksJSONReader
from pathlib import Path    # Gets file names for book + author data

# TODO: we need to move this code into a repository - Luke
data_path = Path('library') / 'adapters' / 'data'
books_file = str(Path(data_path) / "comic_books_excerpt.json")
author_file = str(Path(data_path) / "book_authors_excerpt.json")


reader = BooksJSONReader(books_file, author_file)
reader.read_json_files()
books_db = reader.dataset_of_books

import library.adapters.repository as repo
import library.browse.services as services

browse_blueprint = Blueprint(
    'browse_bp', __name__)


# @browse_blueprint.route('/browse', methods=['GET'])     # shows all books. shouldn't be used
# def browse():
#     books = services.get_books(repo.repo_instance)
#
#     return render_template(
#         'browse/browse.html',
#         books=books,
#     )


@browse_blueprint.route('/browse/<page_num>', methods=['GET'])
def browse_books(page_num):
    # books = services.get_five_books(int(page_num), repo.repo_instance)
    books = services.get_books(repo.repo_instance)
    displayed_books = services.get_five_books(books, int(page_num))

    return render_template(
        'browse/browse.html',
        books=books,
        displayed_books=displayed_books,
        number_of_pages=len(books) // len(displayed_books),
    )


@browse_blueprint.route('/book/<book_id>', methods=['GET'])
def show_book(book_id):
    book_id = int(book_id)

    book = services.get_book(book_id, repo.repo_instance)
    authors = services.display_book_authors(book)
    stock = services.get_book_stock(book_id, repo.repo_instance)
    price = services.get_book_price(book_id, repo.repo_instance)

    return render_template(
        'browse/book.html',
        book=book,
        authors=services.display_book_authors(book),
        stock=stock,
        price=price,
    )
