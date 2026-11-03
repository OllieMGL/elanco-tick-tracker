from datetime import datetime

from load_data import clean_sighting, load_sightings
from models import Sighting


# a valid Elanco record - tests change just the field they care about
def make_record(**changes):
    record = {
        "id": "abc123",
        "date": "2024-06-01T12:00:00",
        "location": "London",
        "species": "Marsh tick",
        "latinName": "Ixodes apronophorus",
    }
    record.update(changes)
    return record


def test_clean_sighting_turns_a_good_record_into_a_sighting():
    sighting = clean_sighting(make_record(location=" London "))

    assert sighting.external_id == "abc123"
    assert sighting.date == datetime(2024, 6, 1, 12, 0)
    assert sighting.location == "London"
    assert sighting.source == "elanco"


def test_clean_sighting_rejects_a_missing_field():
    record = make_record()
    del record["species"]

    assert clean_sighting(record) is None


def test_clean_sighting_rejects_a_bad_date():
    assert clean_sighting(make_record(date="next tuesday")) is None


def test_clean_sighting_rejects_a_future_date():
    assert clean_sighting(make_record(date="2999-01-01T00:00:00")) is None


def test_clean_sighting_rejects_an_unknown_city():
    assert clean_sighting(make_record(location="Atlantis")) is None


def test_load_sightings_skips_duplicates_and_invalid_records(session):
    records = [
        make_record(id="a"),
        make_record(id="a"),                       # duplicate
        make_record(id="b", location="Atlantis"),  # invalid
    ]

    assert load_sightings(records, session) == 1
    assert session.query(Sighting).count() == 1


def test_load_sightings_adds_nothing_when_run_again(session):
    load_sightings([make_record(id="a")], session)

    assert load_sightings([make_record(id="a")], session) == 0
    assert session.query(Sighting).count() == 1
