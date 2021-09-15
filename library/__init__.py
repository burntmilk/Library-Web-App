"""Initialize Flask app."""

from flask import Flask, render_template
from pathlib import Path

from library.adapters.jsondatareader import BooksJSONReader


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # TODO: we need to move this code into a repository - Luke
    data_path = Path('library') / 'adapters' / 'data'
    books_file = str(Path(data_path) / "comic_books_excerpt.json")
    author_file = str(Path(data_path) / "book_authors_excerpt.json")

    reader = BooksJSONReader(books_file, author_file)
    books = reader.read_books_file()

    @app.route('/')
    def home():
        # some_book = create_some_book()
        some_book = books[0]

        # Use Jinja to customize a predefined html page rendering the layout for showing a single book.
        return render_template('simple_book.html', book=some_book)

    return app