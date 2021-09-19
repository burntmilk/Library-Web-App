"""Initialize Flask app."""

from flask import Flask, render_template
from pathlib import Path    # Gets file names for book + author data

import library.adapters.repository as repo
from library.adapters.memory_repository import MemoryRepository, populate


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    data_path = Path('library') / 'adapters' / 'data'

    repo.repo_instance = MemoryRepository()
    populate(data_path, repo.repo_instance)

    with app.app_context():
        # Register blueprints.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .browse import browse
        app.register_blueprint(browse.browse_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

    return app
