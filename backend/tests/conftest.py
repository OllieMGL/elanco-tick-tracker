import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import server
from models import Base


@pytest.fixture
def client(session, monkeypatch):
    # make routes use test db instead of real db
    monkeypatch.setattr(server, "Session", sessionmaker(bind=session.get_bind()))

    # TESTING makes errors inside a route show up in the test instead of 500
    server.app.config.update(TESTING=True)
    return server.app.test_client()

@pytest.fixture
def session():
    # empty in memory db for every test
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    test_session = sessionmaker(bind=engine)()
    yield test_session
    test_session.close()
