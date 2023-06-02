# test_routes.py
import pytest
from .app import app, db  # import your Flask application instance and your database instance
from .models import UserHome  # import your UserHome model

@pytest.fixture
def client():
    app.config['TESTING'] = True

    # If you are using a separate test database
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://home:admin@localhost:5432/test_home_db'

    with app.test_client() as client:
        # Setup: create the database tables
        with app.app_context():
            db.create_all()
        yield client
        # Teardown: drop the database tables
        with app.app_context():
            db.session.remove()
            db.drop_all()

