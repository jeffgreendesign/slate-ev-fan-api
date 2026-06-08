import sys
from pathlib import Path

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.api.endpoints import _load_sources
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


def test_load_sources_reports_missing_file(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    monkeypatch.chdir(tmp_path)

    with pytest.raises(HTTPException) as exc_info:
        _load_sources()

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Source metadata not found"


def test_load_sources_reports_invalid_json(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "slate_sources.json").write_text("{not-json", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    with pytest.raises(HTTPException) as exc_info:
        _load_sources()

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Source metadata is invalid JSON"
