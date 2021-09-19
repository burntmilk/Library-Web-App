from flask import Blueprint, render_template, request, redirect, url_for, session
from math import ceil

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


@browse_blueprint.route('/browse', methods=['GET'])
def browse():
    books_per_page = 5

    page_num = request.args.get('page')  # cursor
    # filter = request.args.get('filter')

    if page_num is None:
        page_num = 1
    else:
        page_num = int(page_num)

    # -- Displaying limited amount of books per page --
    books = services.get_all_books(repo.repo_instance)
    if books_per_page * page_num < len(books):
        books = books[(page_num - 1) * 5: page_num * 5]
    else:
        books = books[(page_num - 1) * 5: len(books)]

    # ----- NAVIGATION BUTTONS -----
    next_page_url = None
    prev_page_url = None
    first_page_url = None
    last_page_url = None

    if page_num-1 > 0:
        prev_page_url = url_for('browse_bp.browse', page=page_num-1)
        first_page_url = url_for('browse_bp.browse')
    if page_num-1 * books_per_page < len(books):
        next_page_url = url_for('browse_bp.browse', page=page_num+1)
        last_page_url = url_for('browse_bp.browse', page=ceil(len(books) / books_per_page))

    return render_template(
        'browse/browse.html',
        books=books,
        next_page_url=next_page_url,
        prev_page_url=prev_page_url,
        first_page_url=first_page_url,
        last_page_url=last_page_url,
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
        authors=authors,
        stock=stock,
        price=price,
    )
