from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_create_and_list_workout():
    payload = {"day": "2026-10-14", "exercise": "pull-up", "sets": 3,
               "reps": 8, "weight_kg": 0, "duration_min": 20}
    created = client.post("/users/chi/workouts", json=payload)
    assert created.status_code == 201
    assert created.json()["volume_kg"] == 0

    listed = client.get("/users/chi/workouts").json()
    assert listed[0]["exercise"] == "pull-up"


def test_weekly_summary_for_active_week():
    res = client.get("/users/anna/summary/weekly", params={"week_start": "2026-10-05"})
    assert res.status_code == 200
    body = res.json()
    assert body["week_end"] == "2026-10-11"
    assert "squat" in body["exercises"]


def test_week_start_must_be_monday():
    res = client.get("/users/anna/summary/weekly", params={"week_start": "2026-10-07"})
    assert res.status_code == 422


def test_weekly_summary_for_empty_week_returns_zeros():
    """KAN-7: binh skipped the week of 2026-10-05 and gets a 500 instead of an empty summary."""
    res = client.get("/users/binh/summary/weekly", params={"week_start": "2026-10-05"})
    assert res.status_code == 200
    body = res.json()
    assert body["sessions"] == 0
    assert body["total_volume_kg"] == 0
    assert body["total_minutes"] == 0
    assert body["avg_minutes_per_session"] == 0
    assert body["exercises"] == []
