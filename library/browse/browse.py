from flask import Blueprint, render_template, request, redirect, url_for, session
from math import ceil

import library.adapters.repository as repo
import library.browse.services as services

browse_blueprint = Blueprint(
    'browse_bp', __name__)


@browse_blueprint.route('/browse', methods=['GET'])
def browse():
    books_per_page = 5

    page_num = request.args.get('page')  # cursor
    if page_num is None:
        page_num = 1
    else:
        page_num = int(page_num)

    # filter = request.args.get('filter')

    books = services.get_all_books(repo.repo_instance)

    # ----- NAVIGATION BUTTONS -----
    next_page_url = None
    prev_page_url = None
    first_page_url = None
    last_page_url = None

    if page_num-1 > 0:
        prev_page_url = url_for('browse_bp.browse', page=page_num-1)
        first_page_url = url_for('browse_bp.browse')
    if page_num * books_per_page < len(books):
        next_page_url = url_for('browse_bp.browse', page=page_num+1)
        last_page_url = url_for('browse_bp.browse', page=ceil(len(books) / books_per_page))

    # -- Displaying limited amount of books per page --
    if books_per_page * page_num < len(books):
        books = books[(page_num - 1) * books_per_page: page_num * books_per_page]
    else:
        books = books[(page_num - 1) * books_per_page: len(books)]

    return render_template(
        'browse/browse.html',
        books=books,
        next_page_url=next_page_url,
        prev_page_url=prev_page_url,
        first_page_url=first_page_url,
        last_page_url=last_page_url,
        page=page_num
    )


@browse_blueprint.route('/book', methods=['GET'])
def show_book():
    book_id = int(request.args.get('book_id'))

    book = services.get_book(book_id, repo.repo_instance)
    stock = services.get_book_stock(book_id, repo.repo_instance)
    price = services.get_book_price(book_id, repo.repo_instance)

    return render_template(
        'browse/book.html',
        book=book,
        stock=stock,
        price=price
    )

@browse_blueprint.route('/review', methods=['GET', 'POST'])
def add_review():
    book_id = int(request.args.get('book_id'))
    book = services.get_book(book_id, repo.repo_instance)

    
    
    # try:
    #     review_text = request.form["review_text"]
    #     rating = request.form["rating"]
    #     services.add_review(book, review_text, rating)
    #     return redirect(url_for('browse_bp.book', book_id))
    # except services.NonExistentBookException:
    #     book_nonexistent = "Book is non-existent"
    # except services.ReviewFormInvalid:
    #     review_form_invalid = "Please fill in all fields before submitting"
    
    return render_template(
        'browse/review.html',
        book=book,
        # book_error=book_nonexistent,
        # form_error=review_form_invalid
    )
