from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS

from cities import CITIES
from db import Session
from get_data import ElancoAPIError
from load_data import refresh_data
from species import SPECIES
from sightings import create_sighting, search_sightings, validate_report
from stats import count_by_calendar_month, count_by_location, count_over_time

app = Flask(__name__)
CORS(app)  # allows React to call on the API despite backend and front end running on differnt localhost ports

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

def refresh_on_startup():
    try:
        added = refresh_data()
        print(f"Elanco data refreshed: {added} new sightings.")
    except ElancoAPIError as error:
        print(f"Could not refresh Elanco data, using saved data instead: {error}")


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


# passes the tick types and possible cities to frontend
@app.route("/api/options", methods=["GET"])
def options():
    return jsonify({
        "cities": CITIES,
        "species": list(SPECIES),
    })


# ERROR HANDLERS ==> FLask can send back a json error response
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Something went wrong. Please try again later."}), 500

if __name__ == "__main__":
    refresh_on_startup()
    app.run(debug=True)
