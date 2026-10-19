# Lightweight Feedback System

[![CI](https://github.com/akhilreddy20/lightweight-feedback-system/actions/workflows/ci.yml/badge.svg)](https://github.com/akhilreddy20/lightweight-feedback-system/actions/workflows/ci.yml)

Managers give structured feedback to their team (strengths, areas to improve, sentiment). Employees see their own feedback history and acknowledge each item.

**Live demo:** https://lightweight-feedback-system-5clk.onrender.com

**Stack:** React (CRA) · FastAPI · MongoDB (Motor, async) · JWT auth · bcrypt · Docker · GitHub Actions

## Features

- Register and log in as **manager** or **employee** (JWT, bcrypt-hashed passwords)
- Managers: see the team, submit feedback, edit their own feedback
- Employees: read their own history (newest first) and acknowledge items
- Role checks on every endpoint, plus per-record checks (employees can only read and acknowledge their own feedback)
- Input validation with Pydantic: roles and sentiment are enums, with length limits on text fields

## Running locally

```bash
# API
cd backend
cp .env.example .env                 # set MONGO_URL and JWT_SECRET
pip install -r requirements.txt
uvicorn main:app --reload            # http://localhost:8000  (docs at /docs)

# UI
REACT_APP_API_URL=http://localhost:8000 npm start   # http://localhost:3000
```

Or with Docker: `docker build -t feedback-api ./backend && docker run -p 8000:8000 --env-file backend/.env feedback-api`

| Env var | Purpose |
|---|---|
| `MONGO_URL` | MongoDB connection string |
| `JWT_SECRET` | Token signing key. If unset, a random key is used and users are signed out on every restart. |
| `TOKEN_TTL_MINUTES` | Token lifetime (default 60) |
| `CORS_ORIGINS` | Comma-separated allowed origins |
| `REACT_APP_API_URL` | Backend URL for the UI |

## Tests

```bash
cd backend
pip install -r requirements-dev.txt
pytest -q
```

The API tests use an in-memory MongoDB mock (`mongomock-motor`). They cover registration and login status codes, validation, token checks, role permissions, and per-record access (an employee can't read or acknowledge someone else's feedback). CI runs them, the frontend build and a Docker build on every push.

## Changelog: bugs fixed

- **Login always failed:** `SECRET_KEY`/`ALGORITHM` were referenced but never defined, so creating a token raised `NameError`. Token config now lives in `config.py`.
- **Registration broke on fresh installs:** `passlib` crashes with `bcrypt>=4.1`. Switched to `bcrypt` directly; existing hashes still verify. Dependencies are now pinned.
- **Wrong status codes:** a broad `except Exception` turned 400/401 into 500. Removed.
- **Passwords in logs:** request bodies were printed during registration. Removed, and a test asserts the password never appears in logs.
- **Anyone could acknowledge anyone's feedback:** acknowledgement is now limited to the feedback's owner.
- **History sorting:** sorted by a `timestamp` that was never written. It's now set on creation.
- The backend URL was hard-coded in 8 places. It's now a single `REACT_APP_API_URL` setting.
