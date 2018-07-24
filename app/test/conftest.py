import logging
import logging.config
import pytest

from core.app import app as flask_app
from core.conf import settings
from model import BaseModel


logging.basicConfig(level=logging.DEBUG)
logging.config.dictConfig(settings['logging'])

settings['database'] = settings['test_database']


@pytest.fixture(scope='session')
def app(request):
    context = flask_app.app_context()
    context.push()

    flask_app.db.create_all()

    def teardown():
        context.pop()
        flask_app.db.drop_all()

    request.addfinalizer(teardown)
    return flask_app


@pytest.fixture(scope='function')
def session(app, request):
    connection = app.db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = app.db.create_scoped_session(options=options)

    app.db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
