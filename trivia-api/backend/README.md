# Trivia API

Backend for the Trivia app (Flask + PostgreSQL).

## Setup
1) From repo root (or this backend folder), create/activate your env (example):
```
python3.10 -m venv .venv
source .venv/bin/activate
```
2) Install deps:
```
pip install -r requirements.txt
```
3) Environment variables (examples):
```
DB_NAME=trivia
DB_USER=postgres
DB_PASSWORD=your_password   # can be blank if using peer auth
DB_HOST=localhost
DB_PORT=5432
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/trivia   # optional override
TEST_DB_NAME=trivia_test
```
4) Databases (default URIs if above not set):
- Dev: `postgresql://postgres@localhost:5432/trivia`
- Test: `postgresql://postgres@localhost:5432/trivia_test`
Create DBs and load sample data:
```
createdb trivia
psql trivia < trivia.psql
createdb trivia_test
```
5) Run the server:
```
export FLASK_APP=flaskr
export FLASK_ENV=development
export DATABASE_URL=postgresql://postgres:o@localhost:5432/trivia
flask run
```
6) Tests:
```
export DATABASE_URL=postgresql://postgres:o@localhost:5432/trivia_test
python test_flaskr.py
```

## API Endpoints
All responses are JSON.

### GET `/categories`
- Returns: `categories` (id: type), `success`
```
{
  "success": true,
  "categories": { "1": "Science", "2": "Art" }
}
```

### GET `/questions?page=<int>`
- Returns paginated (10 per page) `questions`, `total_questions`, `categories`, `current_category`
```
{
  "success": true,
  "questions": [ { "id": 1, "question": "...", "answer": "...", "category": 1, "difficulty": 2 } ],
  "total_questions": 20,
  "categories": { "1": "Science", "2": "Art" },
  "current_category": null
}
```

### DELETE `/questions/<int:question_id>`
- Deletes question id.
- Returns: `success`, `deleted`

### POST `/questions` (create)
- Body: `question`, `answer`, `difficulty` (int), `category` (int)
- Returns: `success`, `created`

### POST `/questions` (search)
- Body: `searchTerm`
- Returns: matching `questions`, `total_questions`, `current_category`

### GET `/categories/<int:category_id>/questions`
- Returns questions for category, plus `total_questions`, `current_category`

### POST `/quizzes`
- Body:
```
{
  "previous_questions": [1, 2],
  "quiz_category": { "id": 0, "type": "click" }   # id 0 => all categories
}
```
- Returns: `question` (random not in previous) or `null` when exhausted, `success`

## Errors
Formatted as:
```
{
  "success": false,
  "error": 404,
  "message": "resource not found"
}
```
Handled: 400, 404, 422, 500.
