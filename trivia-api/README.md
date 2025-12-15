# Trivia App (Udacity FSND)

Backend: Flask + PostgreSQL (see `backend/`).  
Frontend: React (see `frontend/`).

## Prerequisites
- Python 3.10 (venv recommended)
- Node 18+ (for frontend)
- PostgreSQL running locally

## Backend Setup
```bash
cd backend
python3.10 -m venv ../.venv
source ../.venv/bin/activate
pip install -r requirements.txt

# Databases
createdb trivia
psql trivia < trivia.psql
createdb trivia_test

# Run server
export FLASK_APP=flaskr
export FLASK_ENV=development
export DATABASE_URL=postgresql://postgres@localhost:5432/trivia   # adjust if you use a password
flask run

# Tests
export DATABASE_URL=postgresql://postgres@localhost:5432/trivia_test
python test_flaskr.py
```

API endpoint details live in `backend/README.md`.

## Frontend Setup (optional)
```bash
cd frontend
npm install
npm start
```
Frontend runs at http://localhost:3000 and expects the backend at http://127.0.0.1:5000.

## Notes
- `.gitignore` includes venv/node_modules/pyc.
- DB URLs come from env (`DATABASE_URL` / `TEST_DATABASE_URL`). No secrets are hardcoded.
