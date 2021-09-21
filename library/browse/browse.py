from flask import Blueprint, render_template, request, redirect, url_for, session
from math import ceil

from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, ValidationError

import library.adapters.repository as repo
import library.browse.services as services


browse_blueprint = Blueprint(
    'browse_bp', __name__)


@browse_blueprint.route('/browse', methods=['GET', 'POST'])
def browse():
    books_per_page = 5

    page_num = request.args.get('page')  # cursor
    if page_num is None:
        page_num = 1
    else:
        page_num = int(page_num)

    filter_by = request.args.get('filter_by')
    if filter_by is None:
        filter_by = 'title'

    form = SearchForm()
    books = []
    if form.validate_on_submit():
        print(filter_by)
        search_entry = form.search_entry.data
        if filter_by == 'title':
            books = services.get_books_by_title(search_entry, repo.repo_instance)
    else:
        books = services.get_all_books(repo.repo_instance)

    # ----- NAVIGATION BUTTONS -----
    next_page_url = None
    prev_page_url = None
    first_page_url = None
    last_page_url = None

    if page_num-1 > 0:
        prev_page_url = url_for('browse_bp.browse', page=page_num-1, filter_by=filter_by)
        first_page_url = url_for('browse_bp.browse', filter_by=filter_by)
    if page_num * books_per_page < len(books):
        next_page_url = url_for('browse_bp.browse', page=page_num+1, filter_by=filter_by)
        last_page_url = url_for('browse_bp.browse', page=ceil(len(books) / books_per_page), filter_by=filter_by)

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
        page=page_num,
        filter_by=filter_by,
        form=form
    )


@browse_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        return render_template(
            'browse/browse.html',
            filter_by=form.search_entry.data
        )
    else:
        return render_template(
            'browse/search.html',
            form=form,
            handler_url=url_for('browse_bp.search')
        )


@browse_blueprint.route('/book/<int:book_id>')
def show_book(book_id: int):

    book = services.get_book(book_id, repo.repo_instance)
    stock = services.get_book_stock(book_id, repo.repo_instance)
    price = services.get_book_price(book_id, repo.repo_instance)

    return render_template(
        'browse/book.html',
        book=book,
        stock=stock,
        price=price
    )


class SearchForm(FlaskForm):
    search_entry = StringField("Search by:", [DataRequired()])
    submit = SubmitField("Search")
