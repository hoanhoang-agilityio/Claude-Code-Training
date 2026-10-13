"""In-memory workout store. Data resets every time the server restarts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from itertools import count


@dataclass
class Workout:
    id: int
    user_id: str
    day: date
    exercise: str
    sets: int
    reps: int
    weight_kg: float
    duration_min: int

    @property
    def volume_kg(self) -> float:
        return self.sets * self.reps * self.weight_kg


@dataclass
class WorkoutStore:
    _workouts: list[Workout] = field(default_factory=list)
    _ids: count = field(default_factory=lambda: count(1))

    def add(self, user_id: str, day: date, exercise: str, sets: int, reps: int,
            weight_kg: float, duration_min: int) -> Workout:
        workout = Workout(next(self._ids), user_id, day, exercise, sets, reps,
                          weight_kg, duration_min)
        self._workouts.append(workout)
        return workout

    def list_for_user(self, user_id: str, limit: int = 20, offset: int = 0) -> list[Workout]:
        items = sorted((w for w in self._workouts if w.user_id == user_id),
                       key=lambda w: (w.day, w.id), reverse=True)
        return items[offset:offset + limit]

    def between(self, user_id: str, start: date, end: date) -> list[Workout]:
        """Workouts for a user with start <= day < end."""
        return [w for w in self._workouts
                if w.user_id == user_id and start <= w.day < end]

    def clear(self) -> None:
        self._workouts.clear()
        self._ids = count(1)


store = WorkoutStore()
