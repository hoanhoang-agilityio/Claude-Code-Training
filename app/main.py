"""GymLog API — a small practice service for the Claude Code training."""

from __future__ import annotations

from datetime import date

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from app.seed import load_seed
from app.store import store
from app.summary import weekly_summary

app = FastAPI(title="GymLog Coaching API", version="0.1.0")
load_seed(store)


class WorkoutIn(BaseModel):
    day: date
    exercise: str = Field(min_length=1)
    sets: int = Field(gt=0)
    reps: int = Field(gt=0)
    weight_kg: float = Field(ge=0)
    duration_min: int = Field(gt=0)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/users/{user_id}/workouts", status_code=201)
def create_workout(user_id: str, body: WorkoutIn) -> dict:
    w = store.add(user_id, body.day, body.exercise, body.sets, body.reps,
                  body.weight_kg, body.duration_min)
    return {**body.model_dump(mode="json"), "id": w.id, "user_id": user_id,
            "volume_kg": w.volume_kg}


@app.get("/users/{user_id}/workouts")
def list_workouts(user_id: str, limit: int = Query(20, ge=1, le=100),
                  offset: int = Query(0, ge=0)) -> list[dict]:
    return [{"id": w.id, "day": w.day.isoformat(), "exercise": w.exercise,
             "sets": w.sets, "reps": w.reps, "weight_kg": w.weight_kg,
             "duration_min": w.duration_min, "volume_kg": w.volume_kg}
            for w in store.list_for_user(user_id, limit, offset)]


@app.get("/users/{user_id}/summary/weekly")
def get_weekly_summary(user_id: str, week_start: date) -> dict:
    if week_start.weekday() != 0:
        raise HTTPException(422, "week_start must be a Monday")
    return weekly_summary(store, user_id, week_start)
