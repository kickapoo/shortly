import pytest

from app.factory import create_app
from app.models import db as _db


@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    app.app_context = app.app_context()
    app.app_context.push()
    return app


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""

    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()

    return _db

@pytest.fixture
def client():
    app = create_app('testing')
    app.app_context = app.app_context()
    app.app_context.push()
    app.testing = True
    return app.test_client()
