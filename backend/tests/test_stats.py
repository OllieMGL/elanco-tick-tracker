from datetime import datetime

from stats import count_by_calendar_month, count_by_location, count_over_time
from test_sightings import add_sighting


def test_count_by_location(session):
    add_sighting(session, location="London")
    add_sighting(session, location="London")
    add_sighting(session, location="Leeds")

    assert count_by_location(session) == {"London": 2, "Leeds": 1}


def test_count_by_location_uses_the_filters(session):
    add_sighting(session, location="London", species="Marsh tick")
    add_sighting(session, location="London", species="Tree-hole tick")

    assert count_by_location(session, species="Marsh tick") == {"London": 1}


def test_count_over_time_by_month_oldest_first(session):
    add_sighting(session, date=datetime(2024, 7, 2))
    add_sighting(session, date=datetime(2024, 6, 1))
    add_sighting(session, date=datetime(2024, 6, 20))

    assert count_over_time(session, interval="month") == [
        {"period": "2024-06", "count": 2},
        {"period": "2024-07", "count": 1},
    ]


def test_count_over_time_by_week(session):
    add_sighting(session, date=datetime(2024, 6, 3))  # a Monday in ISO week 23
    add_sighting(session, date=datetime(2024, 6, 9))  # the Sunday of the same week

    assert count_over_time(session, interval="week") == [{"period": "2024-W23", "count": 2}]


def test_count_by_calendar_month_combines_years(session):
    add_sighting(session, date=datetime(2022, 6, 1))
    add_sighting(session, date=datetime(2024, 6, 15))  # a different year, same month
    add_sighting(session, date=datetime(2023, 1, 10))

    result = count_by_calendar_month(session)

    assert len(result) == 12  # every month is included
    assert result[0] == {"month": "Jan", "count": 1}
    assert result[1] == {"month": "Feb", "count": 0}
    assert result[5] == {"month": "Jun", "count": 2}


def test_regions_route_counts_per_city_with_filters(client, session):
    add_sighting(session, location="London", date=datetime(2024, 6, 1))
    add_sighting(session, location="Leeds", date=datetime(2020, 1, 1))  # before the start date

    response = client.get("/api/stats/regions?start=2024-01-01")

    assert response.status_code == 200
    assert response.get_json() == {"London": 1}


def test_trends_route_by_week(client, session):
    add_sighting(session, date=datetime(2024, 6, 1))

    response = client.get("/api/stats/trends?interval=week")

    assert response.status_code == 200
    assert response.get_json() == [{"period": "2024-W22", "count": 1}]


def test_trends_route_rejects_an_unknown_interval(client):
    response = client.get("/api/stats/trends?interval=day")

    assert response.status_code == 400


def test_seasonal_route_returns_all_12_months(client, session):
    add_sighting(session, date=datetime(2024, 6, 1))

    body = client.get("/api/stats/seasonal").get_json()

    assert len(body) == 12
    assert body[5] == {"month": "Jun", "count": 1}
