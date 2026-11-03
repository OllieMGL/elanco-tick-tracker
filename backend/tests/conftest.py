import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base
from server import app


@pytest.fixture
def client():
    # TESTING makes errors inside a route show up in the test instead of 500
    app.config.update(TESTING=True)
    return app.test_client()

@pytest.fixture
def session():
    # empty in-memory database for every test
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    test_session = sessionmaker(bind=engine)()
    yield test_session
    test_session.close()
