from flask import Blueprint, render_template

import library.adapters.repository as repo
import library.browse.services as services

browse_blueprint = Blueprint(
    'browse_bp', __name__)


@browse_blueprint.route('/browse', methods=['GET'])
def browse():
    books = services.get_books(repo.repo_instance)
    # books = services.get_five_books(1, repo.repo_instance)

    return render_template(
        'browse/browse.html',
        books=books,
    )


@browse_blueprint.route('/browse/<book_id>', methods=['GET'])
def show_book(book_id):
    book = services.get_book(book_id, repo.repo_instance)

    return render_template(
        'browse/book.html',
        book=book,
    )