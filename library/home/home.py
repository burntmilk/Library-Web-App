from flask import Blueprint, render_template
from flask.globals import request, session
from flask_wtf.form import FlaskForm
from wtforms.fields.core import Field
from wtforms.fields.simple import SubmitField, TextField

import library.adapters.repository as repo
import library.browse.services as services


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        'home/home.html'
    )


@home_blueprint.route('/favourites', methods=['GET', 'POST'])
def favourites():
    user_name = None
    user_favourite_books = []

    form = RemoveFavouritesForm()
    

    
    if 'user_name' in session:
        user_name = session['user_name']

        user_favourite_books = services.get_user_favourite_books(user_name, repo.repo_instance)

    if form.validate_on_submit():
        book_id = int(form.book_id.data)
        services.remove_book_from_user_favourites(user_name, book_id, repo.repo_instance)
        user_favourite_books = services.get_user_favourite_books(user_name, repo.repo_instance)
        return render_template('home/favourites.html', favourites=user_favourite_books, form=form)

    return render_template('home/favourites.html', favourites=user_favourite_books, form=form)

class FavouritesForm(FlaskForm):
    submit = SubmitField('Add to Favourites')

class RemoveFavouritesForm(FlaskForm):
    submit = SubmitField('Remove from Favourites')
    book_id = TextField('book_id')
    
