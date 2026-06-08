import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main import app


def test_sources_endpoint_exposes_public_caveats():
    client = TestClient(app)

    response = client.get("/api/v1/sources")

    assert response.status_code == 200
    data = response.json()
    assert data["official_affiliation"] is False
    assert data["status"] == "preproduction"
    assert "Final MSRP/base price" in data["known_unknowns"]
    assert any(source["url"] == "https://www.slate.auto/en/faq" for source in data["primary_sources"])
