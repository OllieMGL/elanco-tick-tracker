from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from models import Sighting


def make_sighting(external_id="abc123"):
    return Sighting(
        external_id=external_id,
        date=datetime(2024, 6, 1, 12, 0),
        location="London",
        species="Marsh tick",
        latin_name="Ixodes apronophorus",
        source="elanco",
    )


def test_sighting_saves_and_reads_back(session):
    session.add(make_sighting())
    session.commit()

    saved = session.query(Sighting).one()
    assert saved.location == "London"
    assert saved.date == datetime(2024, 6, 1, 12, 0)
    assert saved.source == "elanco"


def test_duplicate_external_id_is_rejected(session):
    session.add(make_sighting("same-id"))
    session.commit()

    session.add(make_sighting("same-id"))
    with pytest.raises(IntegrityError):
        session.commit()
