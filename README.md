# Claude Code Training — GymLog practice app

A small FastAPI service used as the practice codebase for the 15-day Claude training
(dojo.agilityio.dev). Tickets for each day live in this repo's **Issues**, labelled `day-XX`.

## Run it locally

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for the interactive API.

## Run the tests

```bash
pytest -q
```

If `pytest` can't import `app`, run it as `python -m pytest -q` from the repo root.

## API

| Method | Path | What it does |
| ------ | ---- | ------------ |
| GET | `/health` | Liveness check |
| POST | `/users/{user_id}/workouts` | Log a workout |
| GET | `/users/{user_id}/workouts?limit=&offset=` | List a user's workouts, newest first |
| GET | `/users/{user_id}/summary/weekly?week_start=YYYY-MM-DD` | Monday–Sunday summary for one week |

Data is in memory and seeded from `app/seed.py` (users `anna` and `binh`); it resets on restart.
