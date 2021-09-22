from flask import Blueprint, render_template
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        'home/home.html'
    )


@home_blueprint.route('/favourites', methods=['GET', 'POST'])
def favourites():
    return render_template('home/favourites.html')

class FavouritesForm(FlaskForm):
    submit = SubmitField('Add to Favourites')
