# GymLog (Claude Code training repo)

Small FastAPI practice service for the dojo.agilityio.dev training. Data is in memory,
seeded from `app/seed.py`, and resets on restart. Tickets live in Jira project KAN.

## Commands

- Install: `pip install -r requirements.txt` (inside `.venv`)
- Run: `uvicorn app.main:app --reload` (docs at http://127.0.0.1:8000/docs)
- Test: `python -m pytest -q` from the repo root

## Layout

- `app/main.py` routes, `app/store.py` in-memory store, `app/summary.py` weekly summary
- `tests/` pytest; `test_api.py` uses FastAPI `TestClient`

## Conventions

- Bug fix = a failing test first, then the fix, in small commits.
- Commit subject: `type: summary (KAN-N)`, types `fix`, `feat`, `test`, `refactor`, `chore`, `docs`.
- One branch and one PR per ticket. PR description: what changed, why, how it was tested.
- `WorkoutStore.between(start, end)` is end-exclusive; a week is Monday to Sunday.
- Review in the team order: use the `review-checklist` skill before approving a PR.

## Never do

- Never add `Co-Authored-By:` or `Claude-Session:` trailer lines to commit messages.
- Never push to `main` directly or force-push a shared branch; open a PR.
- Never skip, delete or weaken a test to get green.
- Never commit secrets, `.env` files or `.claude/settings.local.json`.
