def test_options_route_lists_cities_and_species(client):
    response = client.get("/api/options")
    body = response.get_json()

    assert response.status_code == 200
    assert len(body["cities"]) == 14
    assert body["cities"]["London"] == {"lat": 51.5074, "lng": -0.1278}
    assert "Not sure" in body["species"]


def test_unknown_url_returns_a_json_404(client):
    response = client.get("/api/nope")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Not found"}


def test_wrong_method_returns_a_json_405(client):
    response = client.delete("/api/sightings")  # the URL exists, but not for DELETE

    assert response.status_code == 405
    assert response.get_json() == {"error": "Method not allowed"}
