import pytest
from server import app


@pytest.fixture
def client():
    # TESTING makes errors inside a route show up in the test instead of 500
    app.config.update(TESTING=True)
    return app.test_client()
