import server
from get_data import ElancoAPIError


def test_options_route_lists_cities_and_species(client):
    response = client.get("/api/options")
    body = response.get_json()

    assert response.status_code == 200
    assert len(body["cities"]) == 14
    assert body["cities"]["London"] == {"lat": 51.5074, "lng": -0.1278}
    assert "Not sure" in body["species"]


def test_api_allows_requests_from_the_frontend(client):
    response = client.get("/api/options", headers={"Origin": "http://localhost:5173"})

    # the header names the frontend's address, telling the browser it's allowed to read the response
    assert response.headers["Access-Control-Allow-Origin"] == "http://localhost:5173"


def test_unknown_url_returns_a_json_404(client):
    response = client.get("/api/nope")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Not found"}


def test_wrong_method_returns_a_json_405(client):
    response = client.delete("/api/sightings")  # the URL exists, but not for DELETE

    assert response.status_code == 405
    assert response.get_json() == {"error": "Method not allowed"}


def test_startup_carries_on_when_elanco_is_down(monkeypatch, capsys):
    def elanco_is_down():
        raise ElancoAPIError("Elanco API unavailable after 3 attempts")

    monkeypatch.setattr(server, "refresh_data", elanco_is_down)

    server.refresh_on_startup()  # the test fails if this raises an error

    assert "using saved data instead" in capsys.readouterr().out
