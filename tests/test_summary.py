from datetime import date

from app.store import WorkoutStore
from app.summary import weekly_summary


def test_empty_week_returns_float_zeros():
    """KAN-7: a week with no workouts must not divide by zero."""
    summary = weekly_summary(WorkoutStore(), "binh", date(2026, 10, 5))

    assert summary["sessions"] == 0
    assert summary["total_minutes"] == 0
    assert summary["exercises"] == []
    assert summary["avg_minutes_per_session"] == 0.0
    assert summary["total_volume_kg"] == 0.0
    assert isinstance(summary["avg_minutes_per_session"], float)
    assert isinstance(summary["total_volume_kg"], float)


def test_average_is_float_for_a_normal_week():
    store = WorkoutStore()
    store.add("anna", date(2026, 10, 6), "squat", 3, 5, 100.0, 40)
    store.add("anna", date(2026, 10, 8), "bench", 3, 5, 60.0, 35)

    summary = weekly_summary(store, "anna", date(2026, 10, 5))

    assert summary["sessions"] == 2
    assert summary["avg_minutes_per_session"] == 37.5
    assert summary["total_volume_kg"] == 2400.0
