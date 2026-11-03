from models import Sighting


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
