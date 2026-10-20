"""Weekly summary calculations."""

from __future__ import annotations

from datetime import date, timedelta

from app.store import WorkoutStore


def weekly_summary(store: WorkoutStore, user_id: str, week_start: date) -> dict:
    """Summarise one training week (Monday to Sunday) for a user."""
    week_end = week_start + timedelta(days=6)  # Sunday
    # between() is end-exclusive, so pass the next Monday to include Sunday (KAN-2).
    workouts = store.between(user_id, week_start, week_end + timedelta(days=1))

    total_volume = sum((w.volume_kg for w in workouts), 0.0)
    total_minutes = sum(w.duration_min for w in workouts)
    # A skipped week is normal: report zeros, not a 500 (KAN-7).
    avg_minutes = round(total_minutes / len(workouts), 1) if workouts else 0.0

    return {
        "user_id": user_id,
        "week_start": week_start.isoformat(),
        "week_end": week_end.isoformat(),
        "sessions": len(workouts),
        "total_volume_kg": round(total_volume, 1),
        "total_minutes": total_minutes,
        "avg_minutes_per_session": avg_minutes,
        "exercises": sorted({w.exercise for w in workouts}),
    }
