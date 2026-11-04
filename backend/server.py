from datetime import datetime

from flask import Flask, jsonify, request

from db import Session
from sightings import search_sightings

app = Flask(__name__)


# turns Sighting from db into plain dict that can be sent as JSON
def sighting_to_dict(sighting):
    return {
        "id": sighting.id,
        "date": sighting.date.isoformat(), # changes date to text
        "location": sighting.location,
        "species": sighting.species,
        "latin_name": sighting.latin_name,
        "source": sighting.source,
    }


def parse_date(text):
    if not text:
        return None
    return datetime.fromisoformat(text)

@app.route("/api/sightings", methods=["GET"])
def list_sightings():
    try:
        start = parse_date(request.args.get("start"))
        end = parse_date(request.args.get("end"))
    except ValueError:
        return jsonify({"error": "start and end must be dates like 2026-11-03"}), 400

    if end:
        end = end.replace(hour=23, minute=59, second=59)  # include the whole end day

    with Session() as session:
        sightings = search_sightings(
            session,
            start=start,
            end=end,
            location=request.args.get("location"),
            species=request.args.get("species"),
        )
        return jsonify([sighting_to_dict(sighting) for sighting in sightings])


if __name__ == "__main__":
    app.run(debug=True)
