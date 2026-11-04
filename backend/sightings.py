from datetime import datetime

from cities import CITIES
from models import Sighting
from species import SPECIES


# finds sighting --> newest first
def search_sightings(session, start=None, end=None, location=None, species=None):
    query = session.query(Sighting)

    # each filter is only added if it was given
    if start:
        query = query.filter(Sighting.date >= start)
    if end:
        query = query.filter(Sighting.date <= end)
    if location:
        query = query.filter(Sighting.location == location)
    if species:
        query = query.filter(Sighting.species == species)

    return query.order_by(Sighting.date.desc()).all()


# returns {field: problem}
def validate_report(data):
    errors = {}

    date_text = data.get("date")
    if not date_text:
        errors["date"] = "Date is required"
    else:
        try:
            if datetime.fromisoformat(date_text) > datetime.now():
                errors["date"] = "Date can't be in the future"
        except (ValueError, TypeError):
            errors["date"] = "Date must be a real date, like 2026-04-30"

    location = data.get("location")
    if not location:
        errors["location"] = "Location is required"
    elif not isinstance(location, str) or location not in CITIES:
        errors["location"] = "Location must be one of the listed cities"

    species = data.get("species")
    if not species:
        errors["species"] = "Species is required"
    elif not isinstance(species, str) or species not in SPECIES:
        errors["species"] = "Species must be one of the listed species"

    return errors


# saves a report as a new sighting
def create_sighting(session, data):
    sighting = Sighting(
        date=datetime.fromisoformat(data["date"]),
        location=data["location"],
        species=data["species"],
        latin_name=SPECIES[data["species"]],  # looked up so users don't have to type it
        source="user",
    )
    session.add(sighting)
    session.commit()
    return sighting
