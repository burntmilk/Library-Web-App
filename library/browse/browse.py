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


browse_blueprint = Blueprint(
    'browse_bp', __name__)


@browse_blueprint.route('/browse', methods=['GET'])
def browse():
    return render_template(
        'browse/browse.html',
        books=books_db
    )
