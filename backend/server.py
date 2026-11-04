from datetime import datetime

from flask import Flask, jsonify, request

from db import Session
from sightings import create_sighting, search_sightings, validate_report
from stats import count_by_calendar_month, count_by_location, count_over_time

app = Flask(__name__)

DATE_ERROR = "start and end must be dates like 2026-11-03"

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

def get_date_range():
    start = parse_date(request.args.get("start"))
    end = parse_date(request.args.get("end"))
    
    if end:
        end = end.replace(hour=23, minute=59, second=59)  # include the whole end day
    return start, end


@app.route("/api/sightings", methods=["GET"])
def list_sightings():
    try:
        start, end = get_date_range()
    except ValueError:
        return jsonify({"error": DATE_ERROR}), 400

    with Session() as session:
        sightings = search_sightings(
            session,
            start=start,
            end=end,
            location=request.args.get("location"),
            species=request.args.get("species"),
        )
        return jsonify([sighting_to_dict(sighting) for sighting in sightings])


@app.route("/api/sightings", methods=["POST"])
def report_sighting():
    data = request.get_json(silent=True)  # None if the body isn't valid JSON
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    errors = validate_report(data)
    if errors:
        return jsonify({"errors": errors}), 400

    with Session() as session:
        sighting = create_sighting(session, data)
        return jsonify(sighting_to_dict(sighting)), 201


# sightings per city
@app.route("/api/stats/regions", methods=["GET"])
def stats_regions():
    try:
        start, end = get_date_range()
    except ValueError:
        return jsonify({"error": DATE_ERROR}), 400

    with Session() as session:
        counts = count_by_location(session, start=start, end=end, species=request.args.get("species"))
        return jsonify(counts)


# sightings per month or week
@app.route("/api/stats/trends", methods=["GET"])
def stats_trends():
    interval = request.args.get("interval", "month")  # month used as a fallback
    if interval not in ("week", "month"):
        return jsonify({"error": "interval must be week or month"}), 400

    try:
        start, end = get_date_range()
    except ValueError:
        return jsonify({"error": DATE_ERROR}), 400

    with Session() as session:
        trend = count_over_time(
            session,
            interval=interval,
            start=start,
            end=end,
            location=request.args.get("location"),
            species=request.args.get("species"),
        )
        return jsonify(trend)


# sightings in each month across all years
@app.route("/api/stats/seasonal", methods=["GET"])
def stats_seasonal():
    with Session() as session:
        months = count_by_calendar_month(
            session,
            location=request.args.get("location"),
            species=request.args.get("species"),
        )
        return jsonify(months)


if __name__ == "__main__":
    app.run(debug=True)
