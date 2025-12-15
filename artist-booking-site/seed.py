from datetime import datetime, timedelta

from app import app
from models import db, Venue, Artist, Show


def seed():
    now = datetime.utcnow()

    venues_data = [
        {
            "name": "The Musical Hop",
            "city": "San Francisco",
            "state": "CA",
            "address": "1015 Folsom Street",
            "phone": "123-123-1234",
            "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
            "facebook_link": "https://www.facebook.com/TheMusicalHop",
            "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5",
            "website_link": "https://www.themusicalhop.com",
            "seeking_talent": True,
            "seeking_description": "Looking for local artists every two weeks.",
        },
        {
            "name": "The Dueling Pianos Bar",
            "city": "New York",
            "state": "NY",
            "address": "335 Delancey Street",
            "phone": "914-003-1132",
            "genres": ["Classical", "R&B", "Hip-Hop"],
            "facebook_link": "https://www.facebook.com/theduelingpianos",
            "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae",
            "website_link": "https://www.theduelingpianos.com",
            "seeking_talent": False,
            "seeking_description": "",
        },
        {
            "name": "Park Square Live Music & Coffee",
            "city": "San Francisco",
            "state": "CA",
            "address": "34 Whiskey Moore Ave",
            "phone": "415-000-1234",
            "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
            "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
            "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7",
            "website_link": "https://www.parksquarelivemusicandcoffee.com",
            "seeking_talent": False,
            "seeking_description": "",
        },
    ]

    artists_data = [
        {
            "name": "Guns N Petals",
            "city": "San Francisco",
            "state": "CA",
            "phone": "326-123-5000",
            "genres": ["Rock n Roll"],
            "facebook_link": "https://www.facebook.com/GunsNPetals",
            "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f",
            "website_link": "https://www.gunsnpetalsband.com",
            "seeking_venue": True,
            "seeking_description": "Looking for shows in the SF Bay Area.",
        },
        {
            "name": "Matt Quevedo",
            "city": "New York",
            "state": "NY",
            "phone": "300-400-5000",
            "genres": ["Jazz"],
            "facebook_link": "https://www.facebook.com/mattquevedo923251523",
            "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5",
            "website_link": "",
            "seeking_venue": False,
            "seeking_description": "",
        },
        {
            "name": "The Wild Sax Band",
            "city": "San Francisco",
            "state": "CA",
            "phone": "432-325-5432",
            "genres": ["Jazz", "Classical"],
            "facebook_link": "",
            "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61",
            "website_link": "",
            "seeking_venue": False,
            "seeking_description": "",
        },
    ]

    with app.app_context():
        venues = []
        for v in venues_data:
            existing = Venue.query.filter_by(name=v["name"], city=v["city"], state=v["state"]).first()
            if existing:
                venues.append(existing)
                continue
            venue = Venue(**v)
            db.session.add(venue)
            venues.append(venue)

        artists = []
        for a in artists_data:
            existing = Artist.query.filter_by(name=a["name"], city=a["city"], state=a["state"]).first()
            if existing:
                artists.append(existing)
                continue
            artist = Artist(**a)
            db.session.add(artist)
            artists.append(artist)

        db.session.flush()

        shows_data = [
            {
                "venue": "The Musical Hop",
                "artist": "Guns N Petals",
                "start_time": now - timedelta(days=200),
            },
            {
                "venue": "Park Square Live Music & Coffee",
                "artist": "Matt Quevedo",
                "start_time": now - timedelta(days=150),
            },
            {
                "venue": "Park Square Live Music & Coffee",
                "artist": "The Wild Sax Band",
                "start_time": now + timedelta(days=120),
            },
            {
                "venue": "Park Square Live Music & Coffee",
                "artist": "The Wild Sax Band",
                "start_time": now + timedelta(days=140),
            },
        ]

        for sd in shows_data:
            venue = next((v for v in venues if v.name == sd["venue"]), None)
            artist = next((a for a in artists if a.name == sd["artist"]), None)
            if not venue or not artist:
                continue
            exists = Show.query.filter_by(venue_id=venue.id, artist_id=artist.id, start_time=sd["start_time"]).first()
            if exists:
                continue
            db.session.add(Show(venue_id=venue.id, artist_id=artist.id, start_time=sd["start_time"]))

        db.session.commit()
        print("Seed complete.")


if __name__ == "__main__":
    seed()
