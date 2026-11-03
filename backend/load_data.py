from datetime import datetime

from cities import CITIES
from models import Sighting

REQUIRED_FIELDS = ["id", "date", "location", "species", "latinName"]

# turns one raw Elanco record into a Sighting, or returns None if it's incomplete
def clean_sighting(record):
    # check for required fields
    for field in REQUIRED_FIELDS:
        value = record.get(field)
        if not isinstance(value, str) or not value.strip():
            return None

    try:
        date = datetime.fromisoformat(record["date"].strip())
    except ValueError:
        return None  # not valid date

    if date > datetime.now():
        return None

    location = record["location"].strip()
    if location not in CITIES:
        return None

    return Sighting(
        external_id=record["id"].strip(),
        date=date,
        location=location,
        species=record["species"].strip(),
        latin_name=record["latinName"].strip(),
        source="elanco", # marks that sighting came from Elanco
    )


# saves valid entries --> skips invalide ones 
def load_sightings(records, session):
    existing_ids = {row.external_id for row in session.query(Sighting.external_id)} # gets already saved ids
    added = 0

    for record in records:
        sighting = clean_sighting(record)

        #skip invalid entries    
        if sighting is None or sighting.external_id in existing_ids:
            continue

        session.add(sighting)
        existing_ids.add(sighting.external_id)
        added += 1

    session.commit()
    return added
