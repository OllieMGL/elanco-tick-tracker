from datetime import datetime

from models import Sighting
from server import sighting_to_dict
from sightings import create_sighting, search_sightings, validate_report


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


def test_sightings_route_returns_filtered_json(client, session):
    add_sighting(session, location="London")
    add_sighting(session, location="Leeds")

    response = client.get("/api/sightings?location=Leeds")

    assert response.status_code == 200
    body = response.get_json()
    assert len(body) == 1
    assert body[0]["location"] == "Leeds"


def test_sightings_route_includes_the_whole_end_day(client, session):
    add_sighting(session, date=datetime(2024, 6, 30, 14, 15))  # afternoon of the end day

    response = client.get("/api/sightings?end=2024-06-30")

    assert len(response.get_json()) == 1


def test_sightings_route_rejects_a_bad_date(client):
    response = client.get("/api/sightings?start=banana")

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_validate_report_accepts_a_good_report():
    report = {"date": "2024-06-30", "location": "London", "species": "Not sure"}

    assert validate_report(report) == {}


def test_validate_report_rejects_missing_bad_and_future_dates():
    assert validate_report({})["date"] == "Date is required"
    assert validate_report({"date": "banana"})["date"] == "Date must be a real date, like 2026-04-30"
    assert validate_report({"date": "2999-01-01"})["date"] == "Date can't be in the future"


def test_validate_report_rejects_missing_and_unknown_location_and_species():
    assert validate_report({})["location"] == "Location is required"
    assert validate_report({})["species"] == "Species is required"

    errors = validate_report({"location": "Atlantis", "species": "Banana tick"})
    assert errors["location"] == "Location must be one of the listed cities"
    assert errors["species"] == "Species must be one of the listed species"


def test_create_sighting_saves_a_user_report(session):
    create_sighting(session, {"date": "2024-06-30", "location": "Leeds", "species": "Marsh tick"})

    saved = session.query(Sighting).one()
    assert saved.location == "Leeds"
    assert saved.latin_name == "Ixodes apronophorus"  # filled in from SPECIES
    assert saved.source == "user"
    assert saved.external_id is None  # only Elanco records have one


def test_report_route_saves_a_good_report(client, session):
    report = {"date": "2024-06-30", "location": "Leeds", "species": "Not sure"}

    response = client.post("/api/sightings", json=report)

    assert response.status_code == 201
    assert response.get_json()["latin_name"] == "Unknown"
    assert session.query(Sighting).count() == 1


def test_report_route_returns_an_error_for_each_bad_field(client, session):
    report = {"date": "2999-01-01", "location": "Atlantis"}  # future date, unknown city, no species

    response = client.post("/api/sightings", json=report)

    assert response.status_code == 400
    assert set(response.get_json()["errors"]) == {"date", "location", "species"}
    assert session.query(Sighting).count() == 0  # nothing saved


def test_report_route_rejects_a_body_that_is_not_json(client):
    response = client.post("/api/sightings", data="hello")

    assert response.status_code == 400
