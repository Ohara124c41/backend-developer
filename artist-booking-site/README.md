# Fyyur: Artist Booking Site

Flask + PostgreSQL app for managing venues, artists, and shows.

## Setup
```bash
cd backend-developer/artist-booking-site
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Database
Set your DB URL (default in config is `postgresql://postgres@localhost:5432/fyyur`):
```bash
export DATABASE_URL=postgresql://postgres@localhost:5432/fyyur   # adjust user/pw/host
createdb fyyur
flask db upgrade    # after setting FLASK_APP=app.py
```

### Run
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
python app.py
```
Visit http://localhost:3000.

## Key Features
- Create/list/edit/delete venues and artists
- Create/list shows; upcoming/past split
- Search venues/artists (partial, case-insensitive)
- Venue/artist detail pages with linked shows

## Endpoints (high level)
- `GET /` home
- `GET /venues` list grouped by city/state; search: `POST /venues/search`
- `GET /venues/<id>` detail; create: `GET/POST /venues/create`; edit: `GET/POST /venues/<id>/edit`; delete: `DELETE /venues/<id>`
- `GET /artists` list; search: `POST /artists/search`
- `GET /artists/<id>` detail; create: `GET/POST /artists/create`; edit: `GET/POST /artists/<id>/edit`
- `GET /shows` list; create: `GET/POST /shows/create`

## Models
- `Venue`, `Artist`, `Show` (Show links Artist↔Venue), genres stored as array, seeking flags, uniqueness on name+city+state.

## Tests
Manual via UI; database migrations via Flask-Migrate (`flask db migrate`, `flask db upgrade`).

## Notes
- `.gitignore` present in repo root.
- Configure secrets/DB via env vars; no hardcoded passwords.
