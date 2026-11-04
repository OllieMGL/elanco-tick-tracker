import calendar
from collections import Counter

from sightings import search_sightings


def count_by_location(session, start=None, end=None, species=None):
    sightings = search_sightings(session, start=start, end=end, species=species)

    # count how many times each city appears ==> {"London": 2, "Leeds": 1}
    return dict(Counter(sighting.location for sighting in sightings))


# the year, month or week a date falls in
def period_label(date, interval):
    if interval == "year":
        return date.strftime("%Y")  # just the year ==> 2024
    if interval == "week":
        return date.strftime("%G-W%V")  # year and week number ==> 2024-W23
    return date.strftime("%Y-%m")  # year and month ==>  2024-06


# sightings per year, month or week
def count_over_time(session, interval="month", start=None, end=None, location=None, species=None):
    sightings = search_sightings(session, start=start, end=end, location=location, species=species)
    counts = Counter(period_label(sighting.date, interval) for sighting in sightings)

    # returns a list of dicts [{"period": "2024-06", "count": 2}, ....]
    return [{"period": period, "count": count} for period, count in sorted(counts.items())]


# total sightings in each calendar month across all years
def count_by_calendar_month(session, location=None, species=None):
    sightings = search_sightings(session, location=location, species=species)
    counts = Counter(sighting.date.month for sighting in sightings)  # month as a number ==> 1-12

    # list of 12 dicts with count across every year added - by month
    return [{"month": calendar.month_abbr[month], "count": counts[month]} for month in range(1, 13)] # calendar.month_abbr[6] == "Jun"
