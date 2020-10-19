from flask import Flask
from .extensions import login_manager, db
from .commands import create_tables
from .models import User, Question
from .routes.auth import auth
from .routes.main import main


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


def create_app(config_file='settings.py'):
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = ''

    app.register_blueprint(main)
    app.register_blueprint(auth)

    with app.app_context():
        from qaflask import routes  # Import routes
        db.create_all()  # Create sql tables for our data models

        return app
