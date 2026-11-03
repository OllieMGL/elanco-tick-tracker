import pytest
import requests

import get_data
from get_data import ElancoAPIError, get_sightings


class FakeResponse:
    def __init__(self, status_code, data=None):
        self.status_code = status_code
        self.data = data

    def json(self):
        return self.data

# monkeypatch swaps out a function for a fake during testing
# ==> automatically puts the original back when the test finished
def fake_elanco(monkeypatch, responses):

    calls = []

    def fake_get(url, timeout):
        calls.append(url)
        result = responses[len(calls) - 1]
        if isinstance(result, Exception):
            raise result
        return result

    monkeypatch.setattr(get_data.requests, "get", fake_get)
    monkeypatch.setattr(get_data.time, "sleep", lambda seconds: None)  # skip the real waits
    return calls


def test_returns_data_on_success(monkeypatch):
    calls = fake_elanco(monkeypatch, [FakeResponse(200, [{"id": "abc"}])])

    assert get_sightings() == [{"id": "abc"}]
    assert len(calls) == 1


def test_retries_on_temporary_errors_then_succeeds(monkeypatch):
    calls = fake_elanco(monkeypatch, [
        requests.ConnectionError(),  # couldnt connect
        FakeResponse(429),           # too many requests
        FakeResponse(200, []),
    ])

    assert get_sightings() == []
    assert len(calls) == 3


def test_gives_up_after_max_attempts(monkeypatch):
    calls = fake_elanco(monkeypatch, [FakeResponse(500)] * 3)

    with pytest.raises(ElancoAPIError):
        get_sightings()
    assert len(calls) == 3


def test_does_not_retry_on_not_found(monkeypatch):
    calls = fake_elanco(monkeypatch, [FakeResponse(404)])

    with pytest.raises(ElancoAPIError):
        get_sightings()
    assert len(calls) == 1
