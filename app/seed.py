"""Demo data loaded at startup so the API has something to show."""

from datetime import date

from app.store import WorkoutStore

SEED = [
    # user_id, day, exercise, sets, reps, weight_kg, duration_min
    ("anna", date(2026, 10, 5), "squat", 5, 5, 80, 45),
    ("anna", date(2026, 10, 7), "bench press", 5, 5, 55, 40),
    ("anna", date(2026, 10, 9), "deadlift", 3, 5, 110, 50),
    ("anna", date(2026, 10, 11), "squat", 5, 5, 82.5, 45),  # Sunday
    ("anna", date(2026, 10, 12), "overhead press", 5, 5, 37.5, 35),
    ("binh", date(2026, 9, 28), "squat", 3, 8, 60, 30),
    ("binh", date(2026, 9, 30), "row", 3, 10, 50, 30),
    # binh skipped the week of 2026-10-05 entirely
    ("binh", date(2026, 10, 13), "bench press", 3, 8, 50, 35),
]


def load_seed(store: WorkoutStore) -> None:
    for user_id, day, exercise, sets, reps, weight, minutes in SEED:
        store.add(user_id, day, exercise, sets, reps, weight, minutes)
