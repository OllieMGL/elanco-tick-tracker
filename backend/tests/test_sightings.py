from datetime import datetime

from models import Sighting
from server import sighting_to_dict
from sightings import search_sightings


# saves a sighting to the test database - tests change just the fields they care about
def add_sighting(session, **changes):
    fields = {
        "date": datetime(2024, 6, 1),
        "location": "London",
        "species": "Marsh tick",
        "latin_name": "Ixodes apronophorus",
        "source": "elanco",
    }
    fields.update(changes)
    session.add(Sighting(**fields))
    session.commit()


def test_search_returns_all_sightings_newest_first(session):
    add_sighting(session, date=datetime(2023, 1, 1))
    add_sighting(session, date=datetime(2024, 1, 1))
    add_sighting(session, date=datetime(2022, 1, 1))

    results = search_sightings(session)

    assert [sighting.date.year for sighting in results] == [2024, 2023, 2022]


def test_search_filters_by_date_range(session):
    add_sighting(session, date=datetime(2023, 12, 31))  # too early
    add_sighting(session, date=datetime(2024, 3, 15))   # inside the range
    add_sighting(session, date=datetime(2024, 7, 1))    # too late

    results = search_sightings(session, start=datetime(2024, 1, 1), end=datetime(2024, 6, 30))

    assert [sighting.date for sighting in results] == [datetime(2024, 3, 15)]


def test_search_filters_by_location_and_species(session):
    add_sighting(session, location="London", species="Marsh tick")
    add_sighting(session, location="London", species="Tree-hole tick")  # wrong species
    add_sighting(session, location="Leeds", species="Marsh tick")       # wrong location

    results = search_sightings(session, location="London", species="Marsh tick")

    assert len(results) == 1
    assert results[0].location == "London"
    assert results[0].species == "Marsh tick"


def test_sighting_to_dict(session):
    add_sighting(session, date=datetime(2024, 6, 1, 14, 30))
    sighting = session.query(Sighting).one()

    assert sighting_to_dict(sighting) == {
        "id": sighting.id,
        "date": "2024-06-01T14:30:00",
        "location": "London",
        "species": "Marsh tick",
        "latin_name": "Ixodes apronophorus",
        "source": "elanco",
    }
